df <- read.csv('../../vegas_dat_merged.csv')

df %>%
  dplyr::filter(home_team == 'denver nuggets') %>%
  dplyr::mutate(home_first_half_pts  = quarter1_x + quarter2_x,
                home_second_half_pts = quarter3_x + quarter4_x,
                away_first_half_pts  = quarter1_y + quarter2_y,
                away_second_half_pts = quarter3_y + quarter4_y) %>%
  dplyr::mutate(first_half_premium   = home_first_half_pts - away_first_half_pts,
                second_half_premium  = home_second_half_pts - away_second_half_pts) %>%
  dplyr::mutate(year = lubridate::year(date)) %>%
  dplyr::group_by(home_team, year) %>%
  dplyr::summarise(first_half_premium  = mean(first_half_premium, na.rm = T),
                   second_half_premium = mean(second_half_premium, na.rm = T), 
                   n())

 df %>%
  dplyr::filter(days_rest_y == 1) %>%
  dplyr::mutate(home_first_half_pts  = quarter1_x + quarter2_x,
                home_second_half_pts = quarter3_x + quarter4_x,
                away_first_half_pts  = quarter1_y + quarter2_y,
                away_second_half_pts = quarter3_y + quarter4_y) %>%
  dplyr::mutate(first_half_premium   = home_first_half_pts - away_first_half_pts,
                second_half_premium  = home_second_half_pts - away_second_half_pts) %>%
  dplyr::mutate(year = lubridate::year(date)) %>%
  dplyr::group_by(year) %>%
  dplyr::summarise(first_half_premium  = mean(first_half_premium, na.rm = T),
                   second_half_premium = mean(second_half_premium, na.rm = T), 
                   half_vs_half_diff   = second_half_premium - first_half_premium, 
                   n())

    
