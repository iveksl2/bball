require(TTR)
library(tidyverse)
library(ggplot2)

pace_df <- read.csv('pace_df.csv')


# Absolute deviance over time: todo: real deviance
pace_deviation <- pace_df %>%
    dplyr::mutate(home_abs_pace_dev  = abs(pace_x - game_pace)) %>%
    dplyr::mutate(away_abs_pace_dev  = abs(pace_y - game_pace)) %>%
    dplyr::mutate(home_pace_dev      = pace_x - game_pace) %>%
    dplyr::mutate(away_pace_dev      = pace_y - game_pace) %>%
    dplyr::mutate(year               = factor(lubridate::year(date))) 

head(pace_deviation)

# Is the pace increasing over time?
pace_deviation %>%
    dplyr::group_by(year) %>%
    dplyr::summarise(pace = mean(game_pace)) %>%
    ggplot(., aes(year, pace)) + geom_point(color = 'blue') +
      ggtitle('Pace over Time')


summary(lm('game_pace ~ pace_x + pace_y', data = pace_deviation))
summary(lm('game_pace ~ .', 
           data = pace_deviation[, setdiff(colnames(pace_deviation), 
                                           c('home_team', 'away_team', 'date'))]))

# Teams with the highest & lowest pace
pace_deviation %>%
    dplyr::group_by(home_team) %>%
    dplyr::summarise(pace = mean(game_pace)) %>%
    dplyr::arrange(desc(pace)) %>%
      ggplot(., aes(reorder(home_team, pace), pace)) + geom_bar(stat = 'identity') + 
        coord_flip() + xlab('team') + ggtitle('pace by team')

pok = pace_deviation %>%
    dplyr::group_by(home_team) %>%
    dplyr::summarise(home_pt_diff = mean(pt_diff_x)) %>%
    dplyr::arrange(., desc(home_pt_diff))

      ggplot(., aes(reorder(home_team, home_pt_diff), home_pt_diff)) + 
        geom_bar(stat = 'identity') + coord_flip() + xlab('team') + 
        ggtitle('point differential')


# 200 observeation simple  
pace_dev_time <- pace_deviation %>% 
    dplyr::select(date, home_abs_pace_dev, away_abs_pace_dev, home_pace_dev, away_pace_dev) %>%
    dplyr::mutate(sma_home_abs_pace_dev  = TTR::SMA(home_abs_pace_dev, 200), 
                  sma_away_abs_pace_dev  = TTR::SMA(away_abs_pace_dev, 200),
                  sma_home_pace_dev      = TTR::SMA(home_pace_dev, 200),
                  sma_away_pace_dev      = TTR::SMA(away_pace_dev, 200)) %>%
    dplyr::select(date, sma_home_abs_pace_dev, sma_away_abs_pace_dev, 
                  sma_home_pace_dev,  sma_away_pace_dev) %>%
    dplyr::mutate(date = as.Date(date))

pace_dev_time %>% tidyr::gather(., 'ma_factor', 'ma', -date) %>% 
    ggplot(., aes(date, ma, color = ma_factor)) + geom_line() %>%
    ggtitle('moving average pace deviation')

#TODO:  
plot(pace_deviation$date, pace_deviation$home_abs_pace_dev, col = 'blue')
lines(pace_deviation$date, pace_deviation$away_abs_pace_dev, col = 'red')

