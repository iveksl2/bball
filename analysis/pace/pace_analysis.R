require(TTR)
library(tidyverse)
library(ggplot2)

pace_df <- read.csv('pace_df.csv')

sigmoid = function(x) {
    1 / (1 + exp(-x))
}

# Absolute deviance over time: todo: real deviance
pace_deviation <- pace_df %>%
    dplyr::mutate(home_abs_pace_dev  = abs(pace_x - game_pace)) %>%
    dplyr::mutate(away_abs_pace_dev  = abs(pace_y - game_pace)) %>%
    dplyr::mutate(home_pace_dev      = pace_x - game_pace) %>%
    dplyr::mutate(away_pace_dev      = pace_y - game_pace) %>%
    dplyr::mutate(date               = as.Date(date)) %>%
    dplyr::mutate(year               = factor(lubridate::year(date))) 

head(pace_deviation)

# Is the pace increasing over time?
pace_deviation %>%
    dplyr::group_by(year) %>%
    dplyr::summarise(pace = mean(game_pace)) %>%
    ggplot(., aes(year, pace)) + geom_point(color = 'blue') +
      ggtitle('Pace over Time')

pace_deviation %>%
    dplyr::group_by(home_team) %>%
    dplyr::summarise(pace = mean(game_pace)) %>%
    dplyr::arrange(desc(pace)) %>%
      ggplot(., aes(reorder(home_team, pace), pace)) + geom_bar(stat = 'identity') + 
        coord_flip() + xlab('team') + ggtitle('pace by team')

pace_deviation %>%
   #dplyr::filter(date > '2014-01-01') %>%
   dplyr::group_by(home_team) %>%
   dplyr::summarise(home_pt_diff = mean(pt_diff_x)) %>%
   ggplot(., aes(reorder(home_team, home_pt_diff), home_pt_diff)) + 
     geom_bar(stat = 'identity') + coord_flip() + xlab('team') + 
     ggtitle('point differential')

# does the home team have a larger effect on pace?
summary(lm('game_pace ~ pace_x + pace_y', data = pace_deviation))

x <- seq(-5, 5, 0.01)
plot(x, sigmoid(x), col = 'blue', main = 'sigmoid')

pace_deviation_interaction <-
    pace_deviation %>%
    dplyr::mutate(home_pt_diff_sigmoid = sigmoid(pt_diff_x),
                  away_pt_diff_sigmoid = sigmoid(pt_diff_y)) %>%
    dplyr::mutate(home_pace_mult_plusminus = pace_x * home_pt_diff_sigmoid,
                  away_pace_mult_plusminus = pace_x * away_pt_diff_sigmoid) 


# does the better team dominate pace?
pace_deviation %>%
    dplyr::mutate(pt_diff_bucket = cut(pt_diff_x, seq(-5, 10, by = 3))) %>%
    dplyr::group_by(pt_diff_bucket) %>%
    dplyr::summarise(mean(home_abs_pace_dev), mean(home_pace_dev), n())


summary(lm('game_pace ~ home_pace_mult_plusminus + away_pace_mult_plusminus', 
           data = pace_deviation_interaction))

with(pace_deviation_interaction, plot(away_pace_mult_plusminus, game_pace))

# SMOOTH_FACTOR observeation simple  
SMOOTH_FACTOR <- 200 
BEGIN_DATE    <- as.Date('2015-01-01')
pace_deviation %>%
    dplyr::filter(date > BEGIN_DATE) %>%
    dplyr::mutate(smooth_game_pace  = TTR::SMA(game_pace, SMOOTH_FACTOR), 
                  smooth_home_pace  = TTR::SMA(pace_x, SMOOTH_FACTOR),
                  smooth_away_pace  = TTR::SMA(pace_y, SMOOTH_FACTOR)) %>%
    dplyr::select(date, smooth_game_pace, smooth_home_pace, smooth_away_pace) %>%
    tidyr::gather(., 'pace_type', 'pace', -date) %>% 
    ggplot(., aes(date, pace, color = pace_type)) + geom_line() + 
    ggtitle('paces')

pace_dev_time <- pace_deviation %>% 
    dplyr::select(date, home_abs_pace_dev, away_abs_pace_dev, home_pace_dev, away_pace_dev) %>%
    dplyr::mutate(sma_home_abs_pace_dev  = TTR::SMA(home_abs_pace_dev, SMOOTH_FACTOR), 
                  sma_away_abs_pace_dev  = TTR::SMA(away_abs_pace_dev, SMOOTH_FACTOR),
                  sma_home_pace_dev      = TTR::SMA(home_pace_dev, SMOOTH_FACTOR),
                  sma_away_pace_dev      = TTR::SMA(away_pace_dev, SMOOTH_FACTOR)) %>%
    dplyr::select(date, sma_home_abs_pace_dev, sma_away_abs_pace_dev, 
                  sma_home_pace_dev,  sma_away_pace_dev) %>%
    dplyr::mutate(date = as.Date(date))

tail(pace_dev_time)

pace_dev_time %>% tidyr::gather(., 'ma_factor', 'ma', -date) %>% 
    ggplot(., aes(date, ma, color = ma_factor)) + geom_line() + 
    ggtitle('moving average pace deviation')

# b2b effect on total score 
pace_df %>%
    dplyr::filter(days_rest_x <= 11) %>%
    dplyr::group_by(days_rest_x) %>%
    dplyr::summarise(total_score = mean(total_score),count =  n()) %>%
    ggplot(., aes(days_rest_x, total_score)) + geom_bar(stat = 'identity')

pace_df %>%
    dplyr::mutate(b2b = ifelse(days_rest_x == 1 | days_rest_y == 1, 1, 0)) %>%
    dplyr::group_by(b2b) %>%
    dplyr::summarise(total_score = mean(total_score))

pace_df %>%
    dplyr::mutate(home_b2b = ifelse(days_rest_x == 1, 1, 0),
                  away_b2b = ifelse(days_rest_y == 1, 1, 0)) %>%
    dplyr::group_by(home_b2b, away_b2b) %>%
    dplyr::summarise(total_score = mean(total_score), 
                     pace = mean(game_pace), count = n())

# nba seems to schedule away team, defense deteriorates
