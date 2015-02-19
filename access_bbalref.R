## first attempt at accessing basketball-reference.com (bible for nba statistics)
library(XML)

url <- 'http://www.basketball-reference.com/'
data <- XML::readHTMLTable(url, stringsAsFactors = FALSE)
## team simple rating system that takes into account point differential & strength of schedule 
dat <- data[['srs_ratings']]

