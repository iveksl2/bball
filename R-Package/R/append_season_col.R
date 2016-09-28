#' Partitions dataframe into different Seasons based on a transition out of playoffs 
#' df -> df
#' @export
append_season_col <- function(df) {
  stopifnot(is.data.frame(df))
  if (!'is_reg_season' %in% names(df)) stop('require is_reg_season column')
  
  season_num         <- 1
  df[['season']] <- season_num
  for (row_idx in 2:NROW(df)) {
     if (df[row_idx, 'is_reg_season'] == TRUE & df[row_idx - 1, 'is_reg_season'] == FALSE) { 
       season_num = season_num + 1
     }     
     df[row_idx, 'season'] <- season_num
  } 
  df
}
