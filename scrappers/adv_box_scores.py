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

Data Dictionary: http://www.basketball-reference.com/about/glossary.html#ast
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
    'New Orleans Pelicans'  : 'NOP', 'New Orleans/Oklahoma City Hornets' : 'NOK',
    'New Orleans Hornets'   : 'NOH', 
    'New York Knicks'       : 'NYK', 'Oklahoma City Thunder' : 'OKC',
    'Orlando Magic'         : 'ORL', 'Philadelphia 76ers'    : 'PHI',
    'Phoenix Suns'          : 'PHO', 'Portland Trail Blazers': 'POR',
    'Sacramento Kings'      : 'SAC', 'San Antonio Spurs'     : 'SAS',
    'Seattle SuperSonics'   : 'SEA', 'Toronto Raptors'       : 'TOR',
    'Utah Jazz'             : 'UTA', 'Washington Wizards'    : 'WAS'
}

EXTRACTED_TEAM_STATS = \
    ['pace', \
    'away_fg', 'away_fga', 'away_fg_per', 'away_3p', 'away_3pa', 'away_3p_per', 'away_ft', 'away_fta', 'away_ft_per', 'away_orb', 'away_drb', 'away_trb', 'away_ast', 'away_stl', 'away_blk', 'away_tov', 'away_pf', 'away_pts', \
    'away_ts_per', 'away_efg_per', 'away_par', 'away_ftr', 'away_orb_per', 'away_drb_per', 'away_trb_per', 'away_ast_per', 'away_stl_per', 'away_blk_per', 'away_tov_per', 'away_usg_per', 'away_ortg', 'away_drtg', \
    'home_fg', 'home_fga', 'home_fg_per', 'home_3p', 'home_3pa', 'home_3p_per', 'home_ft', 'home_fta', 'home_ft_per', 'home_orb', 'home_drb', 'home_trb', 'home_ast', 'home_stl', 'home_blk', 'home_tov', 'home_pf', 'home_pts', \
    'home_ts_per', 'home_efg_per', 'home_par', 'home_ftr', 'home_orb_per', 'home_drb_per', 'home_trb_per', 'home_ast_per', 'home_stl_per', 'home_blk_per', 'home_tov_per', 'home_usg_per', 'home_ortg', 'home_drtg']

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
    # TODO: make dynamic with S3 or DB call
    simple_boxscore_df =  pd.read_csv('/Users/iveksl2/Desktop/bball_data/box_scores.csv') # data driver 
    # Need to use selenium to extract as four_factors html table is poorly structured
    #TODO: make it headless for speed: https://www.youtube.com/watch?v=hktRQNpKktw
    web_driver = webdriver.Chrome(executable_path="/Users/iveksl2/Desktop/chromedriver") 

    adv_box_scores = []
    for i in range(13000, 13782):
        hometeam           = simple_boxscore_df['hometeam'][i]     
        hometeam_bball_ref = BBALL_REF_TEAM_MAP[hometeam]
        game_date          = simple_boxscore_df['date'][i]
        url = gen_adv_box_score_url(game_date, hometeam_bball_ref)              
        print(i, url)
        web_driver.get(url)
        
        selenium_soup = BeautifulSoup(web_driver.page_source, "html.parser")
        pace = selenium_soup.find("td", {"data-stat":"pace"})
        pace = [float(pace.text)]

        soup = soup_from_url(url)
        team_totals = soup.find_all('tfoot') 

        away_basic_team_stats, away_adv_team_stats, home_basic_team_stats, home_adv_team_stats = map(extract_team_tots, team_totals)  
        full_pg_adv_stats = [game_date] + [hometeam] + pace + away_basic_team_stats + away_adv_team_stats + home_basic_team_stats + home_adv_team_stats # append date & hometeam for more robust join
        adv_box_scores.append(full_pg_adv_stats) 

    adv_stats_df = pd.DataFrame(adv_box_scores, columns = ['game_date'] + ['hometeam'] + EXTRACTED_TEAM_STATS) 
    adv_stats_df.to_csv('/Users/iveksl2/Desktop/bball_data/adv_box_scores/adv_box_scores8.csv', index = False) 

    # combine post scrapping 
    adv_boxscore_df  = pd.read_csv('/Users/iveksl2/Desktop/bball_data/adv_box_scores/full_adv_box_scores.csv') 
    full_boxscore_df = pd.merge(simple_boxscore_df, adv_boxscore_df, how = 'left', left_on = ['date', 'hometeam'], right_on = ['game_date', 'hometeam'])
    full_boxscore_df.to_csv('/Users/iveksl2/Desktop/bball_data/adv_box_scores/simple_and_adv_stats.csv', index = False) 

if __name__ == "__main__":
	main()

