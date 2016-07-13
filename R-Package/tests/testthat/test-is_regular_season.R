context('is_regular_season')

test_that('errors on non-date input', {
  expect_error(is_regular_season(33)) 
  expect_error(is_regular_season('this is a string, not a date')) 
  expect_error(is_regular_season(Inf)) 
})

test_that('successfully classifies regular season games', {
  expect_true(is_regular_season(as.Date('2015-01-01')))
  expect_true(is_regular_season(as.Date('2015-10-25')))
  expect_true(is_regular_season(as.Date('2015-10-21'))) # season starts early
  expect_true(is_regular_season(as.Date('2015-03-10'))) 
  expect_true(is_regular_season(as.Date('2015-12-12'))) 
})


test_that('doesent assign playoff or summer league games to regular season', {
  expect_false(is_regular_season(as.Date('2015-03-20')))
  expect_false(is_regular_season(as.Date('2015-05-30')))
  expect_false(is_regular_season(as.Date('2014-09-15')))
})
