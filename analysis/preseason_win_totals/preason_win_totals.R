dat               <- read.csv('full_adv_stats_df.csv')
dat$date          <- as.Date(dat$date)
dat$is_reg_season <- vapply(dat$date, bball::is_regular_season, logical(1))
df                <- bball::append_season_col(dat)

base_df <- df %>%
  subset(., is_reg_season == TRUE) %>%
  dplyr::mutate(season  = as.factor(season)) %>%
  dplyr::select(season, hometeam, home_finalscore, awayteam, away_finalscore) 

home_pt_diff <- base_df %>% 
  dplyr::group_by(season, hometeam) %>% 
  dplyr::summarise(home_num_wins   = sum(home_finalscore > away_finalscore),
                   home_point_diff = mean(home_finalscore - away_finalscore)) 

away_pt_diff <- base_df %>% 
  dplyr::group_by(season, awayteam) %>% 
  dplyr::summarise( away_num_wins   = sum(away_finalscore  > home_finalscore),
                    away_point_diff = mean(away_finalscore - home_finalscore)) 

point_diff_df <- 
  merge(home_pt_diff, away_pt_diff, 
          by.x = c('season', 'hometeam'), 
          by.y = c('season', 'awayteam')) %>%
  dplyr::rename(team = hometeam) %>%
  dplyr::mutate(., num_wins = home_num_wins + away_num_wins, 
                   point_diff = (home_point_diff +  away_point_diff) / 2)       

## Naive Extrapolation
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
  dplyr::mutate(point_diff_lag2 = dplyr::lead(point_diff, 2)) 

print('Naive Model')
naive_mod <- with(pt_diff_lag_df, lm(num_wins ~ point_diff_lag1 + point_diff_lag2))  
summary(naive_mod)
