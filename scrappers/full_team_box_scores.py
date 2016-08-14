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
# key line
soup.find_all('tfoot')


if __name__ == "__main__":
	main()

