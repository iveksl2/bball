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

def soup_from_url(url):
    """ url -> SoupObj ; Instantiate Beautiful Soup Object from a url """    
	response = requests.get(url)
	html     = response.content
	soup     = BeautifulSoup(html, 'lxml')
	return soup

def extract_simple_box_score_stats(team_tot_tags):
    """bs4.element.Tag -> Numeric List; extracts Team Basic Box Score Statistics""" 
    return [float(elem.get_text()) for elem in team_tot_tags.find_all('td')[1:-1]]

def extract_adv_box_score_stats(team_tot_tags):
    """bs4.element.Tag -> Numeric List; extracts Team Advanced Box Score Statistics"""
    return [float(elem.get_text()) for elem in team_tot_tags.find_all('td')[1:]]

def main():
    url = 'http://www.basketball-reference.com/boxscores/201603220BRK.html'
    soup = soup_from_url(url)
    soup.find_all('tfoot')

    team_totals = soup.find_all('tfoot') 
    [float(elem.get_text()) for elem in team_totals[1:-1]] 

    # I don't like this style. If there is a way to make it more consise? 
    away_basic_team_stats = team_totals[0]
    away_adv_team_stats   = team_totals[1]
    home_basic_team_stats = team_totals[2]
    home_adv_team_stats   = team_totals[3]
    
 

if __name__ == "__main__":
	main()

