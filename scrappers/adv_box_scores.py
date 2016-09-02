""" 
http://www.basketball-reference.com/boxscores/201603220BRK.html
"""
from bs4 import BeautifulSoup
from datetime import date
import requests
import re
import pandas as pd
import pdb
import time
from selenium import webdriver
from bs4 import BeautifulSoup

# constants
BBALL_REF_TEAM_MAP = {
    'Atlanta Hawks'         : 'ATL', 'Boston Celtics'        : 'BOS',
    'Brooklyn Nets'         : 'BRK', 'Charlotte Bobcats'     : 'CHA',
    'Charlotte Hornets'     : 'CHO', 'Chicago Bulls'         : 'CHI',
    'Cleveland Cavaliers'   : 'CLE', 'Dallas Mavericks'      : 'DAL',
    'Denver Nuggets'        : 'DEN', 'Detroit Pistons'       : 'DET',
    'Golden State Warriors' : 'GSW', 'Houston Rockets'       : 'HOU',
    'Indiana Pacers'        : 'IND', 'Los Angeles Clippers'  : 'LAC',
    'Los Angeles Lakers'    : 'LAL', 'Memphis Grizzlies'     : 'MEM',
    'Miami Heat'            : 'MIA', 'Milwaukee Bucks'       : 'MIL',
    'Minnesota Timberwolves': 'MIN', 'New Jersey Nets'       : 'NJN',
    'New Orleans Pelicans'  : 'NOP', 'New Orleans/Oklahoma City Hornets' : 'NOH',
    'New York Knicks'       : 'NYK', 'Oklahoma City Thunder' : 'OKC',
    'Orlando Magic'         : 'ORL', 'Philadelphia 76ers'    : 'PHI',
    'Phoenix Suns'          : 'PHO', 'Portland Trail Blazers': 'POR',
    'Sacramento Kings'      : 'SAC', 'San Antonio Spurs'     : 'SAS',
    'Seattle SuperSonics'   : 'SEA', 'Toronto Raptors'       : 'TOR',
    'Utah Jazz'             : 'UTA', 'Washington Wizards'    : 'WAS'
}

def soup_from_url(url):
    """ url -> SoupObj ; Instantiate Beautiful Soup Object from a url """    
	response = requests.get(url)
	html     = response.content
	soup     = BeautifulSoup(html, 'lxml')
	return soup

def extract_team_tots(box_score_tbl_link):
    """ bs4.element.Tag -> list; extracts team totals from box score stats table"""    
    team_tots = [x.get_text() for x in box_score_tbl_link.find_all('td') if x.get_text()]
    return list(map(float, team_tots ))

def main():
    # TODO: make dynamic with S3 or DB call
    bball_data =  pd.read_csv('/Users/iveksl2/Desktop/bball_data/box_scores.csv')
     

    url = 'http://www.basketball-reference.com/boxscores/201603220BRK.html'
    
    # TODO: include pace
    #tmp = soup.find_all('div', { "class" : "table_outer_container"})
    #tmp = soup.find('div', {'id' : 'all_four_factors'}) # think this is the path
    #soup.find('div', {'class' : 'table_outer_container'})
    #tmp = soup.find('table', {'id' : 'div_four_factors'})

    #TODO: make it headless for speed: https://www.youtube.com/watch?v=hktRQNpKktw
    # Need to use selenium as four_factors table containing pace is poorly structured
    driver = webdriver.Chrome(executable_path="/Users/iveksl2/Desktop/chromedriver")
    driver.get(url)
    
    selenium_soup = BeautifulSoup(driver.page_source, "html.parser")
    pace = selenium_soup.find("td", {"data-stat":"pace"})
    float(pace.text)

    # 1 end to end example
    soup = soup_from_url(url)
    team_totals = soup.find_all('tfoot') 

    away_basic_team_stats, away_adv_team_stats, home_basic_team_stats, home_adv_team_stats = map(extract_team_tots, team_totals)  
 

if __name__ == "__main__":
	main()

