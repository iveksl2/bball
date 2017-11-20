# http://www.basketball-reference.com/teams/CLE/2017.html
import pandas as pd
import pdb
import naming_convention_mapper
import re
import requests
import sys
import time
import vegas_scraper

from bs4 import BeautifulSoup
from datetime import date
from dateutil import parser
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

def get_driver(team):
    """team_abbreviation -> selenium_team_driver"""
    URL = 'http://www.basketball-reference.com/teams/' + team + '/2017.html'
    driver = webdriver.Chrome(executable_path='/Users/igor.veksler/Desktop/chromedriver')
    driver.get(URL)
    return driver


# constants
teams = ['ATL',  'BOS', 'BRK',  'CHA', 'CHO',  'CHI', 'CLE',  'DAL',
         'DEN',  'DET', 'GSW',  'HOU', 'IND',  'LAC', 'LAL',  'MEM',
         'MIA',  'MIL', 'MIN',  'NJN', 'NOP',  'NOK', 'NOH', 'NYK',  
         'OKC', 'ORL',  'PHI', 'PHO',  'POR', 'SAC',  'SAS', 'SEA',  
         'TOR', 'UTA',  'WAS' ]


def main():
    #vegas_scrape_date = parser.parse(sys.argv[1])
    vegas_scrape_date  = date(2017,3,10)
    vegas_url = vegas_scraper.vegas_urlize_date(vegas_scrape_date)
    vegas_df = vegas_scraper.get_vegas_lines(vegas_url)
    

    driver = get_driver(team)
    team = teams[5]
    lineup_stats = get_bpm_and_roster(driver)
    
     

