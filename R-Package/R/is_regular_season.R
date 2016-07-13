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
  gm_month <- lubridate::month(date)
  gm_day   <- lubridate::month(date)
  if (gm_month >= REG_SEASON_START_MONTH & gm_month <= REG_SEASON_END_MONTH) {
    if(gm_month == REG_SEASON_END_DAY) { # Dont check start month as any game ~ October is regular season. Specific start days vary 
      if (gm_day > REG_SEASON_END_DAY) FALSE
    }
    else TRUE
  }    
  FALSE
}
