# http://www.basketball-reference.com/teams/CLE/2017.html

from bs4 import BeautifulSoup
from datetime import date
import requests
import re
import pandas as pd
import pdb
import time
#from selenium import webdriver
from bs4 import BeautifulSoup

# constants

teams = ['ATL',  'BOS', 'BRK',  'CHA', 'CHO',  'CHI', 'CLE',  'DAL',
         'DEN',  'DET', 'GSW',  'HOU', 'IND',  'LAC', 'LAL',  'MEM',
         'MIA',  'MIL', 'MIN',  'NJN', 'NOP',  'NOK', 'NOH', 'NYK',  
         'OKC', 'ORL',  'PHI', 'PHO',  'POR', 'SAC',  'SAS', 'SEA',  
         'TOR', 'UTA',  'WAS' ]
team = teams[6]

url = 'http://www.basketball-reference.com/teams/' + team + '/2017.html'

def soup_from_url(url):
    """ url -> SoupObj ; Instantiate Beautiful Soup Object from a url """    
    response = requests.get(url)
    html     = response.content
    soup     = BeautifulSoup(html, 'lxml')
    return soup


soup = soup_from_url(url)
pok = soup.find('div', attrs = {'id' : 'all_per_game'})
pok2 = pok.findChild()
pok3 = pok2.find_next_sibling()


#yo  = soup.find('table', attrs = {'id': 'per_game'})
#yo2  = pok.find('table', attrs = {'id': 'per_game'})
#
#pok2 = pok.findChildren()
#pok2 = pok.children


pok = soup.find('div', attrs = {'id' : 'table'})
pok = soup.find('div', attrs = {'class' : 'table_outer_container'})

pok = soup.find('table', attrs = {'id' : "per_game"})
pok = soup.find('table')

