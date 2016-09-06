""" 
Input: http://www.basketball-reference.com/boxscores/201603220BRK.html
Output: 
pace, 
aFG, aFGA, aFG%, a3P, a3PA, a3P%, aFT, aFTA, aFT%, aORB, aDRB, aTRB, aAST, aSTL, aBLK, aTOV, aPF, aPTS, \
aTS%, aeFG%, aPAr, aFTr, aORB%, aDRB%, aTRB%, aAST%, aSTL%, aBLK%, aTOV%, aUSG%, aORtg, aDRtg, \
hFG, hFGA, hFG%, h3P, h3PA, h3P%, hFT, hFTA, hFT%, hORB, hDRB, hTRB, hAST, hSTL, hBLK, hTOV, hPF, hPTS, \
hTS%, heFG%, hPAr, hFTr, hORB%, hDRB%, hTRB%, hAST%, hSTL%, hBLK%, hTOV%, hUSG%, hORtg, hDRtg
[39.0, 82.0, 0.476, 10.0, 28.0, 0.357, 17.0, 21.0, 0.81, 3.0, 33.0, 36.0, 21.0, 7.0, 5.0, 8.0, 21.0, 105.0, 0.575, 0.537, 0.341, 0.256, 7.3, 84.6, 45.0, 53.8, 7.4, 8.9, 8.1, 100.0, 111.0, 105.7, 34.0, 74.0, 0.459, 8.0, 18.0, 0.444, 24.0, 27.0, 0.889, 6.0, 38.0, 44.0, 21.0, 4.0, 2.0, 16.0, 24.0, 100.0, 0.582, 0.514, 0.243, 0.365, 15.4, 92.7, 55.0, 61.8, 4.2, 3.7, 15.7, 100.0, 105.7, 111.0]
...
etc., 

Data Dictionary embeded wthin html
Prefix_Notation:
h* = home
a* = away
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

EXTRACTED_TEAM_STATS = \ 
    ['pace', \
    'aFG', 'aFGA', 'aFG%', 'a3P', 'a3PA', 'a3P%', 'aFT', 'aFTA', 'aFT%', 'aORB', 'aDRB', 'aTRB', 'aAST', 'aSTL', 'aBLK', 'aTOV', 'aPF', 'aPTS', \
    'aTS%', 'aeFG%', 'aPAr', 'aFTr', 'aORB%', 'aDRB%', 'aTRB%', 'aAST%', 'aSTL%', 'aBLK%', 'aTOV%', 'aUSG%', 'aORtg', 'aDRtg', \
    'hFG', 'hFGA', 'hFG%', 'h3P', 'h3PA', 'h3P%', 'hFT', 'hFTA', 'hFT%', 'hORB', 'hDRB', 'hTRB', 'hAST', 'hSTL', 'hBLK', 'hTOV', 'hPF', 'hPTS', \
    'hTS%', 'heFG%', 'hPAr', 'hFTr', 'hORB%', 'hDRB%', 'hTRB%', 'hAST%', 'hSTL%', 'hBLK%', 'hTOV%', 'hUSG%', 'hORtg', 'hDRtg']

def soup_from_url(url):
    """ url -> SoupObj ; Instantiate Beautiful Soup Object from a url """    
	response = requests.get(url)
	html     = response.content
	soup     = BeautifulSoup(html, 'lxml')
	return soup

def extract_team_tots(box_score_tbl_link):
    """ bs4.element.Tag -> list; extracts team totals from box score stats table"""    
    team_tots = [x.get_text() for x in box_score_tbl_link.find_all('td') if x.get_text()]
    team_tots = team_tots[1:] # Minutes played statistic is redundant on the team level 
    return list(map(float, team_tots))

def gen_adv_box_score_url(game_date, hometeam_bball_ref):
    """Date, Str -> Str; generate advanced box score url using basketball reference notation"""    
    game_date           = pd.Timestamp(game_date)
    url = 'http://www.basketball-reference.com/boxscores/%d%02d%02d0%s.html' % (game_date.year, game_date.month, game_date.day, hometeam_bball_ref) 
    return url

def main():
    # Need to use selenium to extract as four_factors html table is poorly structured
    bball_data =  pd.read_csv('/Users/iveksl2/Desktop/bball_data/box_scores.csv') # data driver 
    web_driver = webdriver.Chrome(executable_path="/Users/iveksl2/Desktop/chromedriver") #TODO: make it headless for speed: https://www.youtube.com/watch?v=hktRQNpKktw

    # TODO: make dynamic with S3 or DB call
    hometeam           = bball_data['hometeam'][0]     
    hometeam_bball_ref = BBALL_REF_TEAM_MAP[hometeam]
    game_date          = bball_data['date'][0]

    url = gen_adv_box_score_url(game_date, hometeam_bball_ref)              
    web_driver.get(url)
    
    selenium_soup = BeautifulSoup(web_driver.page_source, "html.parser")
    pace = selenium_soup.find("td", {"data-stat":"pace"})
    pace = [float(pace.text)]

    soup = soup_from_url(url)
    team_totals = soup.find_all('tfoot') 

    away_basic_team_stats, away_adv_team_stats, home_basic_team_stats, home_adv_team_stats = map(extract_team_tots, team_totals)  
    full_pg_adv_stats = pace + away_basic_team_stats + away_adv_team_stats + home_basic_team_stats + home_adv_team_stats 
    # append date & hometeam for more robust join
    adv_stats_df      = pd.DataFrame([[game_date] + [hometeam] + full_pg_adv_stats], columns = ['game_date'] + ['hometeam'] + EXTRACTED_TEAM_STATS) 

if __name__ == "__main__":
	main()

