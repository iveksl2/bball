raw_box_scores_df <- read.csv('box_scores.csv')
names(raw_box_scores_df) <- #TODO: fix upstream in python scrapping code
  c('date', 'away_team', 'away_quarter1','away_quarter2','away_quarter3','away_quarter4', 'away_finalscore',
            'home_team', 'home_quarter1','home_quarter2','home_quarter3','home_quarter4', 'home_finalscore') 

box_score_df <- 
  dplyr::mutate(raw_box_scores_df, date = as.Date(date)) %>%
  dplyr::mutate(., hm_crt_adv = home_finalscore - away_finalscore) 
  
hm_crt_pt_diff <- box_score_df[['hm_crt_adv']]
hist(hm_crt_pt_diff , col = 'yellow', 
      main = 'Final score Point differential 2006-2016', 
      xlab = 'Home Team Final Score - Away Team Final Score', breaks = 85)

summary(hm_crt_pt_diff)
