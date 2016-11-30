import pandas as pd
import numpy as  np
from sklearn.ensemble import RandomForestClassifier 

def re_arrange_first_col(df, col_name):
    col_lst = df.columns.tolist()
    col_lst.remove(col_name)
    new_col_lst = [col_name] + col_lst 
    return df[new_col_lst]

def wide_to_long(df, team):
	''' Coverts wide dataframen(hometeam & awayteam) by stacking on a team basis'''
        # todo: DRY
	home     = df[df.home_team == team]
	home_sub = home.iloc[:, home.columns.str.contains('date|home|pace|id')]
	home_sub.columns = home_sub.columns.str.replace('home_', '')

	away     = df[df.away_team == team]
	away_sub = away.iloc[:, away.columns.str.contains('date|away|pace|id')]
	away_sub.columns = away_sub.columns.str.replace('away_', '')

	long_df  = pd.concat([home_sub, away_sub])
	return long_df

def shift_create_rolling_stats(df):
	df.date = df.date.shift(-1) # Since this is RHS table
	df.index = df['date'] 
	df.drop(['date', 'team_spread', 'team_moneyline'], axis = 1, inplace = True)
	df_rolling = df.rolling(min_periods = 10, window = 80).mean()
	return df_rolling

# --------------------   workflow   --------------------------
pd.set_option('display.width', 150) # todo: put this in a config file to persist 
df = pd.read_csv('/Users/igor.veksler/Desktop/bball/game_data_and_vegas.csv')
pd.options.display.max_columns = 50
df['game_id']     = range(df.shape[0])
df['date']        = pd.to_datetime(df['date'])
df['away_team']   = df['away_team'].str.lower() #todo, do this upsream
df['total_score'] = df['home_finalscore'] + df['away_finalscore']
df                = re_arrange_first_col(df, 'game_id')
long_gs  = wide_to_long(df, 'golden state warriors')
long_cle = wide_to_long(df, 'cleveland cavaliers')

df_gs_rolling    = shift_create_rolling_stats(long_gs)
df_cle_rolling   = shift_create_rolling_stats(long_cle)

rolling_team_avgs = {}
for team in set(df.home_team.values):
    rolling_team_avgs[team] = wide_to_long(df, team)
    rolling_team_avgs[team]['game_id']  = rolling_team_avgs[team]['game_id'].astype(str) # hack to prevent rolling game_id 
    rolling_team_avgs[team].drop(['date', 'team_spread', 'team_moneyline'], axis = 1, inplace = True) 
    rolling_team_avgs[team] = rolling_team_avgs[team].rolling(min_periods = 10, window = 80).mean()
    rolling_team_avgs[team]['game_id']  = rolling_team_avgs[team]['game_id'].astype(int) # hack to prevent rolling game_id 
    rolling_team_avgs[team]['prev_game_id'] = rolling_team_avgs[team]['game_id'].shift(-1) # RHS Table
    rolling_team_avgs[team].dropna(inplace = True)
    rolling_team_avgs[team]['prev_game_id'] = rolling_team_avgs[team]['prev_game_id'].astype(int)


vegas_data = df.loc[:, ['game_id', 'date', 'home_team', 'away_team', 'total_score', 'over_under']]
vegas_data.index = vegas_data['date']

rolling_avg_concat = pd.concat(rolling_team_avgs.values(), ignore_index = True) 
vegas_with_rolling_figs = vegas_data.copy() 
vegas_with_rolling_figs  =  pd.merge(vegas_with_rolling_figs, rolling_avg_concat , left_on = ['home_team', 'game_id'],   right_on = ['team', 'prev_game_id'], how = 'left')
vegas_with_rolling_figs  =  pd.merge(vegas_with_rolling_figs, rolling_avg_concat , left_on = ['away_team', 'game_id_x'],   right_on = ['team', 'prev_game_id'], how = 'left')


# ------ modeling workflow to transfer -------------
o_u_dat = vegas_with_rolling_figs.dropna()
rf = RandomForestClassifier(n_estimators = 100)
features = list(set(vegas_with_rolling_figs.columns) - set(['game_id_x', 'game_id_y', 'home_team', 'away_team', 'team_x', 'team_y', 'date', 'game_date', 'game_date_x', 'game_date_y'])) 
target   = o_u_dat.total_score 
rf.fit(o_u_dat[features], target)
