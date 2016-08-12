""" 
"""
from bs4 import BeautifulSoup
from datetime import date
import requests
import re
import pandas as pd
import pdb
import time

def make_soup(url):
	response = requests.get(url)
	html     = response.content
	soup     = BeautifulSoup(html, 'lxml')
	return soup


def main():
start_date = date(2010, 1, 1)  
end_date   = date(2016, 7, 1) 
date_range = pd.date_range(start_date, end_date, freq = 'D')

soup       = make_soup(url)


if __name__ == "__main__":
	main()

