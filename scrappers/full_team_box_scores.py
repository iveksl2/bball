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

def main():
    # TODO: to make dynamic with S3 or DB call
    bball_data =  pd.read_csv('/Users/iveksl2/Desktop/bball_data/box_scores.csv')
     

    # TODO: include pace
    # 1 end to end example
    url = 'http://www.basketball-reference.com/boxscores/201603220BRK.html'
    soup = soup_from_url(url)
    team_totals = soup.find_all('tfoot') 

    # TODO: DRY
    away_basic_team_stats = [float(elem.get_text()) for elem in team_totals[0].find_all('td')[:-1]]   
    away_adv_team_stats   = [float(elem.get_text()) for elem in team_totals[1].find_all('td')]   
    home_basic_team_stats = [float(elem.get_text()) for elem in team_totals[2].find_all('td')[:-1]]   
    home_adv_team_stats   = [float(elem.get_text()) for elem in team_totals[3].find_all('td')]   
    
   
 

if __name__ == "__main__":
	main()

