'''
The following program uses following python modules:
bs4 		for scraping purposes
urllib2 	for requesting url content and reading response
csv		for writing data to csv file


Final Output
scraped.csv file in the current working directory.
'''


from bs4 import BeautifulSoup 
import urllib2
import csv

csvwriter = csv.writer(file('scraped.csv', 'ab'))
csvwriter.writerow(['date', 'home_team', 'away_team', 'home_team_spread', 'away_team_spread', 'home_team_moneyline', 'away_team_moneyline', 'over_under'])

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
    home_team_name = each_home.find('a').text
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

    csvwriter.writerow([date_content, home_team_name, away_team_name, home_team_spread, away_team_spread, home_team_moneyline, away_team_moneyline, over_under])


def main(url):
    '''
    url: param string
    Uses urllib2 to request and read content. 
    Uses bs4 to get the rows for nba data
    Passes each home team row and away team row to scrape_individual_contents method for further scraping.
    '''
    response = urllib2.urlopen(url)
    response = response.read()
    soup = BeautifulSoup(response)
    date_content = (soup.find('div', attrs={'class':'date'})).text
    nba_table_area = soup.find('div', attrs={'class':'rightShadow'})
    away_team_tr = nba_table_area.find_all('tr', attrs={'class':'odd'})
    home_team_tr = nba_table_area.find_all('tr', attrs={'class':'even'})
    
    for each_away, each_home in zip(away_team_tr, home_team_tr):
        scrape_individual_contents(each_away, each_home, date_content)    

if __name__ == '__main__':
    url = "http://www.scoresandodds.com/grid_20160129.html"
    main(url)






