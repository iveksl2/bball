library(lubridate)
label_seasons <- function(df) {
  stopifnot('reg_season' %in% names(df)) 
  seasonal_vec <- vector(length = nrow(df))
  season <- 1
  for (i in seq_len(nrow(df))) {
    if (df[i, 'reg_season'] == TRUE & df[max(1, i - 1), 'reg_season'] == FALSE) season = season + 1
    seasonal_vec[i] <- season
  }
  df[['season']] <- seasonal_vec  
  df
}

raw_box_scores_df <- read.csv('box_scores.csv')

names(raw_box_scores_df) <- #TODO: fix upstream in python scrapping code
  c('date', 'away_team', 'away_quarter1','away_quarter2','away_quarter3','away_quarter4', 'away_finalscore',
            'home_team', 'home_quarter1','home_quarter2','home_quarter3','home_quarter4', 'home_finalscore') 

box_scores_df <- 
  dplyr::mutate(raw_box_scores_df, date = as.Date(date)) %>%
  dplyr::mutate(., hm_crt_pt_diff  = home_finalscore - away_finalscore,
                   year            = lubridate::year(date),
                   first_half_pts  = home_quarter1 + home_quarter2 + away_quarter1 + away_quarter2,
                   second_half_pts = home_quarter3 + home_quarter4 + away_quarter3 + away_quarter4,
                   total_pts       = away_finalscore + home_finalscore,
                   reg_season      = vapply(box_scores_df$date, is_regular_season, logical(1)),  # function is not vectorized yet. Therefore `vapply` necessary
                   reg_season      = factor(ifelse(reg_season, 'Regular_Season', 'Playoffs'), levels = c('Regular_Season', 'Playoffs'))) %>%  
  label_seasons(.) 

# How much is home court advantage worth?
summary(box_scores_df[['hm_crt_pt_diff']])
hist(box_scores_df[['hm_crt_pt_diff']] , col = 'yellow', 
      main = 'Final Score point differential 2006-2016', 
      xlab = 'Home Team Final Score - Away Team Final Score', breaks = 85)
hist(box_scores_df[box_scores_df$reg_season == TRUE, 'hm_crt_pt_diff'] , col = 'blue', breaks = 85, xlim = c(-20, 20))
hist(box_scores_df[box_scores_df$reg_season == FALSE, 'hm_crt_pt_diff'] , col = 'green', breaks = 85, xlim = c(-20, 20))

# ^ Bimodal distrubtion

box_scores_df %>%
  dplyr::group_by(year) %>%
  dplyr::summarise(start_date = min(date), end_date = max(date))
#TODO: no 1 quarter how a significantly higher scoring output or home and awauy than any other

# conditional on a win the home team tends to win by 11 points
mean(abs(box_scores_df[['hm_crt_pt_diff']]) <= 5)
subset(box_scores_df, hm_crt_pt_diff > 0) %>% .[['hm_crt_pt_diff']] %>% summary
subset(box_scores_df, hm_crt_pt_diff < 0) %>% .[['hm_crt_pt_diff']] %>% summary # conditional on loss

# Does home court advantge matter differ in the regular season vs the playoffs?
box_scores_df %>%
  dplyr::group_by(reg_season) %>%
  summarise(hm_crt_pt_diff = mean(hm_crt_pt_diff)) %>%
  ggplot2::ggplot(., aes(reg_season, hm_crt_pt_diff)) + geom_bar(stat = 'identity') 

# Does Advantage diminishing over time?
box_scores_df %>%
  dplyr::group_by(year, reg_season) %>%
  summarise(hm_crt_pt_diff = mean(hm_crt_pt_diff)) %>%
  ggplot2::ggplot(., aes(year, hm_crt_pt_diff, color = reg_season)) + 
  geom_line() + ylab('Home Team Total Points - Away Team Total Points') + 
  ggtitle('Home Court Advantage - Point Differential over Time')


# ------- Total points scored over time --------
box_scores_df %>%
  dplyr::group_by(year, reg_season) %>%
  summarise(total_pts = mean(total_pts)) %>%
  ggplot(., aes(year, total_pts , color = reg_season)) + 
  geom_line() + geom_point() + 
  geom_smooth(se = FALSE, method = 'lm', size = .5, linetype="dotted") + 
  ggtitle('Total Pts Scored Over Time (Regular Season vs Playoffs)')

box_scores_df %>%
  dplyr::group_by(reg_season) %>%
  summarise(total_pts = mean(total_pts)) %>%
  ggplot(., aes(reg_season, total_pts))  +  geom_bar(stat = 'identity', aes(fill = reg_season)) + 
  coord_cartesian(ylim=c(175, 225)) + ylab('Average Total Pts Scored') + 
  ggtitle('Are more points scored in the Regular Season or Post Season?')

box_scores_df %>%
  ggplot(., aes(total_pts, fill = reg_season))  + geom_density(alpha = .5) 

# - Which Half Scores more pts? - 
box_scores_df %>% 
  dplyr::select(first_half_pts, second_half_pts) %>% 
  tidyr::gather(., half, pts) %>%
  dplyr::group_by(half) %>% 
  dplyr::summarise(ave_pts = mean(pts)) %>%
  ggplot(., aes(half, ave_pts, fill = half)) + geom_bar(stat = 'identity') +
  coord_cartesian(ylim=c(85, 115)) + ggtitle('Which Half Scores more Points?')
#TODO: Make comment how this is despite foul trouble

box_scores_df %>% 
  dplyr::select(first_half_pts, second_half_pts) %>% 
  tidyr::gather(., half, pts) %>%

# - What % of the time do overtime games occur? 
box_scores_df %>% 
  dplyr::mutate(overtime = (first_half_pts + second_half_pts != total_pts)) %>%
  .[['overtime']] %>% mean 



