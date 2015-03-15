### first attempt at accessing basketball-reference.com (bible for nba statistics)
### GET DATA
require(plyr)
library(XML)

#' Retrieves current snapshot of team SRS data (taken from bball-ref)
#' team simple rating system that takes into account point differential & strength of schedule 
#' @export
get_srs <- function() {
  url <- 'http://www.basketball-reference.com/'
  data <- XML::readHTMLTable(url, stringsAsFactors = FALSE)
  dat <- data[['srs_ratings']]
}

#' Access snapshot player RPM for 1 page from espn
get_partial_rpm <- function(page_num) {
  url <- paste0("http://espn.go.com/nba/statistics/rpm/_/page/", page_num, "/sort/RPM")
  data <- XML::readHTMLTable(url, stringsAsFactors = FALSE)
  data[[1]]
}

#' Fetch full Real Plus-Minus for all players (taken from espn)
#' Note. This is a snapshot as of the state of world when the function was called.
#' @export 
get_full_rpm <-  function() {
  ## currently espn has 13 pages worth of player data. Not very Robust code 
  plyr::ldply(seq(13), fetch_partial_rpm, .progress = 'text')
  ## convert to numeric  -> decided to do here instead of helper for performance optimization 
  numeric_vars <- c( "GP", "MPG", "ORPM", "DRPM", "RPM", "WAR")
  full_rpm[, numeric_vars] <- sapply(full_rpm[, numeric_vars], as.numeric)
}

