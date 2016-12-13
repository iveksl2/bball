import pandas as pd
import numpy as  np
from sklearn.ensemble import RandomForestClassifier 

def create_train_test_col(df, train_per = .8):
    num_rows   = df.shape[0]
    num_train  = int(train_per * df.shape[0])
    return ['train'] * num_train + ['test'] * (num_rows - num_train)

def re_arrange_first_col(df, col_name):
    col_lst = df.columns.tolist()
    col_lst.remove(col_name)
    new_col_lst = [col_name] + col_lst 
    return df[new_col_lst]

def wide_to_long(df, team):
	''' Coverts wide dataframen(hometeam & awayteam) by stacking on a team basis'''
        # todo: DRY
	home_df       = df[df.home_team == team]
	home_df_cols  = home_df.iloc[:, home_df.columns.str.contains('date|home|pace|id')]
	home_df_cols.columns = home_df_cols.columns.str.replace('home_', '')

	away_df       = df[df.away_team == team]
	away_df_cols  = away_df.iloc[:, away_df.columns.str.contains('date|away|pace|id')]
	away_df_cols.columns = away_df_cols.columns.str.replace('away_', '')

	long_df  = pd.concat([home_df_cols, away_df_cols]) 
        long_df.drop(['team_spread', 'team_moneyline', 'game_date'], axis = 1, inplace = True)
        stacked_df = long_df.sort_values(by = ['date']) 
	return stacked_df 

# --------------------   workflow   --------------------------
pd.set_option('display.width', 150) # todo: put this in a config file to persist 
df = pd.read_csv('/Users/igor.veksler/Desktop/bball/game_data_and_vegas.csv')
df = df[df.reg_season == True]
df['game_id']     = range(df.shape[0])
pd.options.display.max_columns = 50
df['date']        = pd.to_datetime(df['date'])
df['away_team']   = df['away_team'].str.lower() #todo, do this upsream
df['home_team']   = df['home_team'].str.lower() #todo, do this upsream
df['total_score'] = df['home_finalscore'] + df['away_finalscore']
df                = re_arrange_first_col(df, 'game_id')

long_gs  = wide_to_long(df, 'golden state warriors')
long_cle = wide_to_long(df, 'cleveland cavaliers')

# todo: break out
rolling_team_avgs = {}
for team in set(df.home_team.values): 
    rolling_team_avgs[team] = wide_to_long(df, team)
    rolling_team_avgs[team]['game_id']  = rolling_team_avgs[team]['game_id'].astype(str) # hack to prevent rolling game_id 
    rolling_team_avgs[team]['date']  = rolling_team_avgs[team]['date'].astype(str) 
    rolling_team_avgs[team] = rolling_team_avgs[team].ewm(alpha = .15).mean()
    rolling_team_avgs[team]['game_id']   = rolling_team_avgs[team]['game_id'].astype(int) # hack to prevent rolling game_id 
    rolling_team_avgs[team]['date']      = pd.to_datetime(rolling_team_avgs[team]['date'])   
    rolling_team_avgs[team]['days_rest'] = rolling_team_avgs[team]['date'] - rolling_team_avgs[team]['date'].shift(1)
    rolling_team_avgs[team].dropna(inplace = True)
    rolling_team_avgs[team]['days_rest'] = rolling_team_avgs[team]['days_rest'].apply(lambda x: x.days)
    rolling_team_avgs[team]['shifted_back_game_id'] = rolling_team_avgs[team]['game_id'].shift(-1) # RHS Table
    rolling_team_avgs[team]['days_rest'] = rolling_team_avgs[team]['days_rest'].shift(-1) 
    rolling_team_avgs[team].dropna(inplace = True)
    rolling_team_avgs[team]['days_rest'] = rolling_team_avgs[team]['days_rest'].astype(int)
    rolling_team_avgs[team]['shifted_back_game_id'] = rolling_team_avgs[team]['shifted_back_game_id'].astype(int)
    rolling_team_avgs[team].drop(['date'], axis = 1, inplace = True) 


vegas_data = df[['game_id', 'date', 'home_team', 'away_team', 'total_score', 'over_under']]
vegas_data.index = vegas_data['date']

rolling_avg_concat = pd.concat(rolling_team_avgs.values(), ignore_index = True) 
rolling_avg_concat = rolling_avg_concat.sort_values(by = ['game_id']) 

vegas_dat_merged = vegas_data.copy() 
vegas_dat_merged  =  pd.merge(vegas_dat_merged, rolling_avg_concat , left_on = ['home_team', 'game_id'],   right_on = ['team', 'shifted_back_game_id'], how = 'left')
vegas_dat_merged  =  pd.merge(vegas_dat_merged, rolling_avg_concat , left_on = ['away_team', 'game_id_x'],   right_on = ['team', 'shifted_back_game_id'], how = 'left')

# ------ mod  -------------
o_u_dat = vegas_dat_merged.dropna()
o_u_dat = o_u_dat[o_u_dat.over_under > 100] 

o_u_dat['partition'] = create_train_test_col(o_u_dat)

train_dat    = o_u_dat[o_u_dat.partition == 'train']
train_target = train_dat.total_score 

test_dat    = o_u_dat[o_u_dat.partition == 'test']
test_target = test_dat.total_score 

rf = RandomForestClassifier(n_estimators = 1000)

features            = list(set(vegas_dat_merged.columns) - set(['game_id_x', 'game_id_y', 'home_team', 'away_team', 'team_x', 'team_y', 'date', 'game_date', 'game_date_x', 'game_date_y', 'partition', 'date_x', 'date_y', 'total_score', 'shifted_back_game_id_y', 'shifted_back_game_id_x'])) 

rf.fit(train_dat[features], train_target)

test_dat['model_o_u'] = rf.predict(test_dat[features])

val_df  = test_dat[['total_score', 'over_under', 'model_o_u']]
val_df['dif'] = val_df['model_o_u'] - val_df['over_under']


diff_threshold = 0 
val_df['dif'] = val_df['model_o_u'] - val_df['over_under']
bet_over_df  = val_df[val_df.dif > diff_threshold]
bet_under_df = val_df[val_df.dif < -diff_threshold]

print(np.mean(bet_over_df.total_score > bet_over_df.over_under))
print(np.mean(bet_under_df.total_score < bet_under_df.over_under))

