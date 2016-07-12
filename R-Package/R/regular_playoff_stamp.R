REG_SEASON_START_MONTH <- 10
REG_SEASON_START_DAY   <- 25 
REG_SEASON_END_MONTH   <- 3 
REG_SEASON_END_DAY     <- 16 

#' Whether the nba game date falls within regular season. 
#' Games outside of this fall within the playoffs. Note there are lockout seasons not currently handled
#'
#' @export
is_regular_season <- function(date) {
  stopifnot(is.Date(date))
   
}
