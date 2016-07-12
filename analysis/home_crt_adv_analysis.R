library(lubridate)

raw_box_scores_df <- read.csv('box_scores.csv')

names(raw_box_scores_df) <- #TODO: fix upstream in python scrapping code
  c('date', 'away_team', 'away_quarter1','away_quarter2','away_quarter3','away_quarter4', 'away_finalscore',
            'home_team', 'home_quarter1','home_quarter2','home_quarter3','home_quarter4', 'home_finalscore') 

box_scores_df <- 
  dplyr::mutate(raw_box_scores_df, date = as.Date(date)) %>%
  dplyr::mutate(., hm_crt_adv = home_finalscore - away_finalscore,
                   year       = lubridate::year(date)) 
  
hm_crt_pt_diff <- box_scores_df[['hm_crt_adv']]
# How much is home court advantage worth?
summary(hm_crt_pt_diff)
hist(hm_crt_pt_diff , col = 'yellow', 
      main = 'Final score Point differential 2006-2016', 
      xlab = 'Home Team Final Score - Away Team Final Score', breaks = 85)
# ^ Bimodal distrubtion

# Is home court worth more in the playoffs
# Changing over time

box_scores_df %>%
  dplyr::group_by(year) %>%
  dplyr::summarise(start_date = min(date), end_date = max(date))


