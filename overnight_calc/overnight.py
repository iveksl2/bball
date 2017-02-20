# http://www.basketball-reference.com/teams/CLE/2017.html
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

teams = ['ATL',  'BOS', 'BRK',  'CHA', 'CHO',  'CHI', 'CLE',  'DAL',
         'DEN',  'DET', 'GSW',  'HOU', 'IND',  'LAC', 'LAL',  'MEM',
         'MIA',  'MIL', 'MIN',  'NJN', 'NOP',  'NOK', 'NOH', 'NYK',  
         'OKC', 'ORL',  'PHI', 'PHO',  'POR', 'SAC',  'SAS', 'SEA',  
         'TOR', 'UTA',  'WAS' ]
team = teams[6]

url = 'http://www.basketball-reference.com/teams/' + team + '/2017.html'

def get_soup(url):
    """ url -> SoupObj ; Instantiate Beautiful Soup Object from a url """    
    response = requests.get(url)
    html     = response.content
    soup     = BeautifulSoup(html, 'lxml')
    return soup

# beautiful soup approach (doesent work)
soup = get_soup(url)

driver = webdriver.Chrome(executable_path='/Users/igor.veksler/Desktop/chromedriver')

driver.get(url)
# mpg
advanced_rows = driver.find_elements_by_xpath('//*[@id="advanced"]/tbody/tr')
advanced_rows[0].find_elements_by_xpath('child::*')[1].text
# bpm
per_game_rows = driver.find_elements_by_xpath('//*[@id="per_game"]/tbody/tr')
per_game_rows[0].find_elements_by_xpath('child::*')[1].text

##selenium approach (doesent work)
#chrome_driver = webdriver.Chrome("/Users/igor.veksler/Desktop/chromedriver") 
#chrome_driver.get('http://www.basketball-reference.com/teams/OKC/2017.html')
#selenium_soup = BeautifulSoup(chrome_driver.page_source, "html.parser")
#pace = selenium_soup.find("td", {"data-stat":"pace"})


