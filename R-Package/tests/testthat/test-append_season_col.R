context('append_season_col')

test_that('dataframe contains is_reg_season col', {
  expect_error(append_season_col(iris)) 
})

test_that('successfully classifies regular season games', {
  df <- data.frame(is_reg_season = c(T, T, T, F, F, T, T, F, T , F, T)) 
  expect_equal(append_season_col(df)$season, c(1, 1, 1, 1, 1, 2, 2, 2, 3, 3, 4))
})



