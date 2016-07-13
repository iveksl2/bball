library(lubridate)

raw_box_scores_df <- read.csv('box_scores.csv')

names(raw_box_scores_df) <- #TODO: fix upstream in python scrapping code
  c('date', 'away_team', 'away_quarter1','away_quarter2','away_quarter3','away_quarter4', 'away_finalscore',
            'home_team', 'home_quarter1','home_quarter2','home_quarter3','home_quarter4', 'home_finalscore') 

box_scores_df <- 
  dplyr::mutate(raw_box_scores_df, date = as.Date(date)) %>%
  dplyr::mutate(., hm_crt_pt_diff = home_finalscore - away_finalscore,
                   year       = lubridate::year(date)) 
  
# How much is home court advantage worth?
summary(box_scores_df[['hm_crt_pt_diff']])
hist(box_scores_df[['hm_crt_pt_diff']] , col = 'yellow', 
      main = 'Final Score point differential 2006-2016', 
      xlab = 'Home Team Final Score - Away Team Final Score', breaks = 85)
# ^ Bimodal distrubtion

# Is home court worth more in the playoffs
# Changing over time

box_scores_df %>%
  dplyr::group_by(year) %>%
  dplyr::summarise(start_date = min(date), end_date = max(date))
#TODO: no 1 quarter how a significantly higher scoring output or home and awauy than any other

# conditional on a win the home team tends to win by 11 points
mean(abs(box_scores_df[['hm_crt_pt_diff']]) <= 5)
subset(box_scores_df, hm_crt_pt_diff > 0) %>% .[['hm_crt_pt_diff']] %>% summary
subset(box_scores_df, hm_crt_pt_diff < 0) %>% .[['hm_crt_pt_diff']] %>% summary # conditional on loss
