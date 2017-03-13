# http://www.basketball-reference.com/teams/CLE/2017.html
from bs4 import BeautifulSoup
from datetime import date
import requests
import re
import pandas as pd
import pdb
import time
from selenium import webdriver

def get_bpm_and_roster(team_base_html):
    advanced_table = team_base_html.find_elements_by_xpath('//*[@id="advanced"]/tbody/tr')

    player_stats = []        
    for xml_head in advanced_table: 
        player_name, GP, MP, OBPM, DBPM =  map(lambda x: xml_head.find_elements_by_xpath('child::*')[x].text, [1,3,4,23,24])    
        player_stats.append([player_name, GP, MP, OBPM, DBPM])

    bpm_df = pd.DataFrame(player_stats, columns = ['player_name','GP','MP','OBPM','DBPM']) 
    bpm_df = bpm_df.apply(lambda x: pd.to_numeric(x, errors='ignore'))
    bpm_df['MPG'] = bpm_df['MP'] / bpm_df['GP']  
    return bpm_df    

# constants
teams = ['ATL',  'BOS', 'BRK',  'CHA', 'CHO',  'CHI', 'CLE',  'DAL',
         'DEN',  'DET', 'GSW',  'HOU', 'IND',  'LAC', 'LAL',  'MEM',
         'MIA',  'MIL', 'MIN',  'NJN', 'NOP',  'NOK', 'NOH', 'NYK',  
         'OKC', 'ORL',  'PHI', 'PHO',  'POR', 'SAC',  'SAS', 'SEA',  
         'TOR', 'UTA',  'WAS' ]

def main()
    team = teams[5]
    URL = 'http://www.basketball-reference.com/teams/' + team + '/2017.html'
    driver = webdriver.Chrome(executable_path='/Users/igor.veksler/Desktop/chromedriver')
    driver.get(URL)


