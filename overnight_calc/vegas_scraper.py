#!/usr/local/bin/python3.6/
'''
Duplicate code from scrapper repo
#TODO: Import as library
'''


from bs4 import BeautifulSoup 
from datetime import date
from dateutil import parser
import csv
import pandas as pd
import requests
import sys

#csvwriter = csv.writer(file('scraped.csv', 'ab'))
#csvwriter.writerow(['date', 'home_team', 'away_team', 'home_team_spread', 'away_team_spread', 'home_team_moneyline', 'away_team_moneyline', 'over_under'])

def get_spread_overunder(away_team_current, home_team_current):
    '''
    Compares the current values in away team row and home team row. 
    Acts according to the specification
    '''
    if away_team_current > home_team_current:
        home_team_spread = home_team_current
        away_team_spread = -1 * home_team_current
        over_under = away_team_current
    else:
        away_team_spread = away_team_current
        home_team_spread = -1 * away_team_current
        over_under = home_team_current
    return [home_team_spread, away_team_spread, over_under]

def scrape_individual_contents(each_away, each_home, date_content):
    '''
    Parses each home team row and away team row collectively to get contents to write to csv file individually.
    get_spread_overunder method is called from here for getting correct data fields. 
    '''
    away_team_name = each_away.find('a').text
    away_team_name = ' '.join(away_team_name.split(' ')[1:3]) 
    home_team_name = each_home.find('a').text
    home_team_name = ' '.join(home_team_name.split(' ')[1:3]) 
    away_team_tds = each_away.find_all('td')
    home_team_tds = each_home.find_all('td')
    away_team_current = (away_team_tds[3]).text
    home_team_current = (home_team_tds[3]).text
    away_team_current = (away_team_current.split(' '))[0]
    home_team_current = (home_team_current.split(' '))[0]
    away_team_current = (away_team_current.split('u'))[0]
    home_team_current = (home_team_current.split('u'))[0]
    away_team_current = float(away_team_current)
    home_team_current = float(home_team_current)
    home_team_spread, away_team_spread, over_under = get_spread_overunder(away_team_current, home_team_current)
    away_team_moneyline = (away_team_tds[4]).text 
    home_team_moneyline = (home_team_tds[4]).text
    return([date_content, home_team_name, away_team_name, home_team_spread, away_team_spread, home_team_moneyline, away_team_moneyline, over_under])

def get_vegas_lines(url):
    response = requests.get(url).content 
    soup = BeautifulSoup(response)
    date_content = soup.find('div', attrs={'class':'date'}).text
    nba_table_area = soup.find('div', attrs={'class':'rightShadow'})
    away_team_tr = nba_table_area.find_all('tr', attrs={'class':'odd'})
    home_team_tr = nba_table_area.find_all('tr', attrs={'class':'even'})
    
    vegas_lines = []     
    for each_away, each_home in zip(away_team_tr, home_team_tr):
        vegas_line = scrape_individual_contents(each_away, each_home, date_content)    
        vegas_lines.append(vegas_line)            
    
    return(pd.DataFrame(vegas_lines, columns = ['date', 'home_team', 'away_team', 'home_spread', 'away_spread', 'home_moneyline', 'away_moneyline', 'over_under']))
    
def vegas_urlize_date(date):
    """Date -> vegas_line_endpoint_url"""
    base_url = "http://www.scoresandodds.com/grid_"
    vegas_url = base_url + "%d%02d%02d.html" % (date.year, date.month, date.day)
    return vegas_url

def main(url):
    a_date = date(2017,3,10)
    vegas_url = vegas_urlize_date(a_date)
    get_vegas_lines(vegas_url)
    

if __name__ == '__main__':
    url = "http://www.scoresandodds.com/grid_20170310.html"
    main(url)






