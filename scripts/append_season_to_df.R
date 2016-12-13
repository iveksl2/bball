library(bball)
library(lubridate)
df <- read.csv('/Users/igor.veksler/Desktop/bball/game_data_and_vegas.csv')

df[['date']] <- as.Date(df[['date']])
df[['reg_season']] <- vapply(df$date, bball::is_regular_season, logical(1))

write.csv(df, '/Users/igor.veksler/Desktop/bball/game_data_and_vegas.csv', row.names = F)
