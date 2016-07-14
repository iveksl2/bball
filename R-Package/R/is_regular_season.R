REG_SEASON_START_MONTH <- 10
REG_SEASON_START_DAY   <- 25 
REG_SEASON_END_MONTH   <- 4 
REG_SEASON_END_DAY     <- 16 

#' Whether the nba game date falls within regular season. 
#' Games outside of this fall within the playoffs. Note there are lockout seasons not currently handled
#'
#' @export
is_regular_season <- function(gm_date) {
  stopifnot(is.Date(gm_date))
  gm_month <- lubridate::month(gm_date)
  gm_day   <- lubridate::day(gm_date)
  if (gm_month %in% c(11, 12, 1, 2, 3)) TRUE 
  else if (identical(gm_month, REG_SEASON_START_MONTH) & gm_day >= REG_SEASON_START_DAY) TRUE 
  else if (identical(gm_month, REG_SEASON_END_MONTH)   & gm_day <= REG_SEASON_END_DAY)   TRUE
  else FALSE
}
