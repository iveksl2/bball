---
title: "Point Analysis"
output:
  md_document
---



# How much is home court advantage worth?

```
##    Min. 1st Qu.  Median    Mean 3rd Qu.    Max. 
## -58.000  -6.000   4.000   3.093  12.000  55.000
```

![plot of chunk home_crt_analysis_overall](figure/home_crt_analysis_overall-1.png)
 * Interesting to note above is a bimodal distribution with close games occuring relatively infrequently. 
   This would imply it would be advantegeous to bet moneyline rather than Point spread on smaller spreads.  


```
## [1] 0.2755043
```

```
##    Min. 1st Qu.  Median    Mean 3rd Qu.    Max. 
##    1.00    6.00   10.00   11.73   16.00   55.00
```
  * Conditional on a win the home team tends to win by 11 points

# Does home court advantge matter differ in the regular season vs the playoffs?
![plot of chunk home_crt_reg_vs_playoffs](figure/home_crt_reg_vs_playoffs-1.png)

# Is home court advantage diminishing over time? 
![plot of chunk home_crt_over_time](figure/home_crt_over_time-1.png)

# Total points scored Analysis
![plot of chunk total_pts](figure/total_pts-1.png)
  * Less points per game are scored within playoffs. 
    Likely due to diminished pace or more conservative foul calls by refereers. TODO: Can verify both hypothesis

![plot of chunk total_pts_over_time](figure/total_pts_over_time-1.png)
  * General trajectory of the league is increasing point totals

# Which Half Scores mores points?
![plot of chunk half_analysis](figure/half_analysis-1.png)
  * Despite a team's being in foul trouble counter intuitively within 2nd half slightly less points are scored

# What % of the time do overtime games occur? 

```
## [1] 0.06247279
```


