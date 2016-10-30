import pandas as pd
import numpy as  np

pd.set_option('display.width', 150) # todo: find out how to have this sit in config file. save vim settings

df = pd.read_csv('/Users/igor.veksler/Desktop/bball/game_data_and_vegas.csv')
# --------------- preprocessing -------------------
df['date']     = pd.to_datetime(df['date'])
df['awayteam'] = df['awayteam'].str.lower()

def subset_df_team_date_range(df, team, start_date = '2000-01-01', 
                                        end_date = '2099-01-01'):
    df_team_filtered = df[(df['hometeam'] == team) | (df['awayteam'] == team)]
    df_date_filtered = df_team_filtered[(df_team_filtered['date'] >= start_date) & (
                                         df_team_filtered['date'] <= end_date)]
    return df_date_filtered

team = 'golden state warriors'
subset_df_team_date_range(df, team, 
        start_date = '2015-01-01', end_date = '2099-01-01'):
                              
    kk
