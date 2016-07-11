""" 
Scrapes basketball reference box score page. Return(s):
Date,Home Team,Quarter 1,Quarter 2,Quarter 3,Quarter 4,Final Score,Away Team,Quarter 1,Quarter 2,Quarter 3,Quarter 4,Final Score

I.E.
url  = 'http://www.basketball-reference.com/boxscores/index.cgi?month=3&day=22&year=2016'
'2016-03-22', 'Charlotte Hornets', '25', '21', '21', '38', '105', 'Brooklyn Nets', '14', '22', '28', '36', '100'
etc.
requirement: Python 3
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

def get_box_score_team_lnks(soup):
	box_scores_tbl = soup.find('div', attrs = {'id': 'boxes'})
	team_lnks      = box_scores_tbl.find_all('a', href  = re.compile('teams'))
	return team_lnks

def parse_box_table(quartet_links, date = ''):
	""" each basketball-reference box score passed links to team names and quarter scores
	as 4 seperate links. Will return Home Team + scores & Away Team + scores in a list""" 
	home_team_name   = [quartet_links[0].get_text()]
	away_team_name   = [quartet_links[1].get_text()]
	home_team_scores = extract_pt_scores(quartet_links[2])
	away_team_scores = extract_pt_scores(quartet_links[3])
	return [date] + home_team_name + home_team_scores + away_team_name + away_team_scores
	
def extract_pt_scores(wide_table_team_link):
	""" extracts 1st through 4th quarter & total point scored """
	scores = [score.get_text() for score in wide_table_team_link.findParent().findNextSiblings()] 
	return scores[0:4] + [scores[-1]] # ignores overtime for simplicity

def get_all_box_scores_on_pg(all_team_lnks, date_str = '', verbose = False):
	full_pg_box_scores = []
	for idx in range(0, len(all_team_lnks), 4):		
		full_pg_box_scores.append(parse_box_table(all_team_lnks[idx:idx + 4 + 1], date_str))
	if (verbose): print('Date:', date_str, 'successfully parsed', len(full_pg_box_scores), 'games')
	return full_pg_box_scores


def main():
	start_date = date(2010, 1, 1)  
	end_date   = date(2016, 7, 1) 
	date_range = pd.date_range(start_date, end_date, freq = 'D')

	nba_box_scores = []
	for idx in range(len(date_range)):
		url = 'http://www.basketball-reference.com/boxscores/index.cgi' \
			  '?month=' + str(date_range.month[idx]) + \
			  '&day='   + str(date_range.day[idx])   + \
			  '&year='  + str(date_range.year[idx])
	
		soup       = make_soup(url)
		team_lnks  = get_box_score_team_lnks(soup) 
		if (team_lnks == []): continue
		date_str   = str(date_range[idx].date())
		nba_box_scores.extend(get_all_box_scores_on_pg(team_lnks, date_str, verbose = True))
		time.sleep(.1) # curteousness not to spam

	#print(*nba_box_scores, sep = '\n')
	box_score_df = pd.DataFrame(nba_box_scores, columns = ['date','awayteam','away_quarter1','away_quarter2','away_quarter3','away_quarter4','away_finalscore','hometeam','home_quarter1','home_quarter2','home_quarter3','home_quarter4','home_finalscore'])
	box_score_df.to_csv('box_scores.csv', index = False)	


if __name__ == "__main__":
	main()

