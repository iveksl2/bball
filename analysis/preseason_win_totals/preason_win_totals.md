



# Forecasting presason win totals
### Naive Extrapolation
```{r naive_extrapolation, echo = FALSE)
point_diff_df %>%
  dplyr::mutate(season  = as.numeric(season)) %>%
      ggplot(aes(season, point_diff, color = team)) + 
        geom_point() + 
        stat_smooth(method = 'lm', se = FALSE, size = 1) + 
        facet_wrap(~ team) + 
        ggtitle('Point differential last 10 seasons') + 
        theme(legend.position = "none")

team_name_changes  <- c('Charlotte Bobcats', 'New Jersey Nets', 'New Orleans Hornets', 
                        'New Orleans Hornets', 'New Orleans/Oklahoma City Hornets', 
                        'Seattle SuperSonics')

pt_diff_lag_df <- point_diff_df %>%
  dplyr::select(season, team, num_wins, point_diff) %>% 
  dplyr::arrange(team, season) %>% 
  subset(., !team %in% team_name_changes) %>%
  dplyr::mutate(point_diff_lag1 = dplyr::lead(point_diff)) %>% 
  dplyr::mutate(point_diff_lag2 = dplyr::lead(point_diff, 2)) %>% 
  dplyr::mutate(point_diff_lag3 = dplyr::lead(point_diff, 3)) %>%
  dplyr::mutate(num_wins_lag1   = dplyr::lead(num_wins, 1)) 
```
