## first attempt at accessing basketball-reference.com (bible for nba statistics)
# TODO: Refactor dog shit code below you lazy schmuck

### GET DATA
require(plyr)
library(XML)
library(magrittr)
library(dplyr)

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
  full_rpm <- plyr::ldply(seq(13), get_partial_rpm, .progress = 'text')
  ## convert to numeric  -> decided to do here instead of helper for performance optimization 
  numeric_vars <- c( "GP", "MPG", "ORPM", "DRPM", "RPM", "WAR")
  full_rpm[, numeric_vars] <- sapply(full_rpm[, numeric_vars], as.numeric)
  full_rpm
}

#' Retrieves Team Level offensive and Defensive Efficiency 
#' @export
get_eff <- function() {
  url <- 'http://espn.go.com/nba/hollinger/teamstats/_/sort/defensiveEff/order/false'
  data <- XML::readHTMLTable(url, stringsAsFactors = FALSE, header = TRUE, as.data.frame = TRUE)
  dat <- data[[1]]
  names(dat) <- dat[1, ]  
  names(dat) <- sub(" ", ".", names(dat))
  dat <- dat[-1, ]
}

open_table <- function() {
  url <- 'http://espn.go.com/nba/hollinger/teamstats/_/sort/defensiveEff/order/false'
  browseURL(url) 
}
#' Calculates total Expeted Points Scored of 2 Arbitrary Teams 
#' @export
exp_pts <- function(teamA, teamB) {
  dat <- get_eff()
  dat2 <- dat[dat$TEAM %in% c(teamA, teamB), ] ## TODO can make it more versatile with grep  
  stopifnot(nrow(dat2) == 2)
  a_pace <- as.numeric(as.character(dat2[dat2$TEAM == teamA, 'PACE'])) 
  a_off_eff<- as.numeric(as.character(dat2[dat2$TEAM == teamA, 'OFF.EFF'])) 
  a_def_eff<- as.numeric(as.character(dat2[dat2$TEAM == teamA, 'DEF.EFF'])) 
  b_pace <- as.numeric(as.character(dat2[dat2$TEAM == teamB, 'PACE'])) 
  b_off_eff <- as.numeric(as.character(dat2[dat2$TEAM == teamB, 'OFF.EFF'])) 
  b_def_eff <- as.numeric(as.character(dat2[dat2$TEAM == teamB, 'DEF.EFF'])) 
  ## (above) ugly code
  a_exp_pts <- a_pace / 100 * a_off_eff * ( b_def_eff / 100) * (a_pace / 100)   
  b_exp_pts <- b_pace / 100 * b_off_eff * ( a_def_eff / 100) * (b_pace / 100) 
  a_exp_pts + b_exp_pts
}


