## first attempt at accessing basketball-reference.com (bible for nba statistics)
require(plyr)
library(XML)

url <- 'http://www.basketball-reference.com/'
data <- XML::readHTMLTable(url, stringsAsFactors = FALSE)
dat <- data[['srs_ratings']] # team simple rating system that takes into account point differential & strength of schedule 

## Access full RPM 
fetch_partial_rpm <- function(page_num) {
  url <- paste0("http://espn.go.com/nba/statistics/rpm/_/page/", page_num, "/sort/RPM")
  data <- XML::readHTMLTable(url, stringsAsFactors = FALSE)
  data[[1]]
}

full_rpm <- plyr::ldply(seq(13), fetch_partial_rpm, .progress = 'text')
numeric_vars <- c( "GP", "MPG", "ORPM", "DRPM", "RPM", "WAR")
## cast correct columns as numeric
full_rpm[, numeric_vars] <- sapply(full_rpm[, numeric_vars], as.numeric)

arrange(full_rpm , -RPM)
