require(TTR)
library(tidyverse)

pace_df <- read.csv('pace_df.csv')

# Absolute deviance over time: todo: real deviance
pace_deviation <- pace_df %>%
    dplyr::mutate(home_abs_pace_dev  = abs(pace_x - game_pace)) %>%
    dplyr::mutate(away_abs_pace_dev  = abs(pace_y - game_pace)) %>%
    dplyr::mutate(home_pace_dev      = pace_x - game_pace) %>%
    dplyr::mutate(away_pace_dev      = pace_y - game_pace) %>%
    dplyr::mutate(year               = factor(lubridate::year(date))) 

head(pace_deviation)

summary(lm('game_pace ~ pace_x + pace_y', data = pace_deviation))

# 200 observeation simple  
pok2 <- pace_deviation %>% 
    dplyr::select(date, home_abs_pace_dev, away_abs_pace_dev) %>%
    dplyr::mutate(sma_home_abs_pace_dev = TTR::SMA(home_abs_pace_dev, 200), 
                  sma_away_abs_pace_dev = TTR::SMA(away_abs_pace_dev, 200),
                  sma_abs_pace_dev      = TTR::SMA(home_pace_dev, 200),
                  sma_abs_pace_dev      = TTR::SMA(away_pace_dev, 200)) 

# Is the pace increasing over time?
pace_deviation %>%
    dplyr::group_by(year) %>%
    dplyr::summarise(pace = mean(game_pace))

# Teams with the highest & lowest pace
pok2 <- pace_deviation %>%
    dplyr::group_by(home_team) %>%
    dplyr::summarise(pace = mean(game_pace)) %>%
    dplyr::arrange(desc(pace))

#TODO:  
plot(pace_deviation$date, pace_deviation$home_abs_pace_dev, col = 'blue')
lines(pace_deviation$date, pace_deviation$away_abs_pace_dev, col = 'red')

