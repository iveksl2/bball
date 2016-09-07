---
title: "Point Analysis"
output:
  md_document
---



### How much is home court advantage worth?

```
## Final Home Score - Final Away Team Score:
```

```
##    Min. 1st Qu.  Median    Mean 3rd Qu.    Max. 
## -58.000  -6.000   4.000   3.093  12.000  55.000
```

![plot of chunk home_crt_analysis_overall](figure/home_crt_analysis_overall-1.png)
 * *Analysis: Interesting to note above is a bimodal distribution with close games occuring relatively infrequently. 
   This would imply it would be advantageous to bet moneyline rather than Point spread on smaller spreads.*  

##### Contingent on win, how many points does the home court team typically win by?

```
##    Min. 1st Qu.  Median    Mean 3rd Qu.    Max. 
##    1.00    6.00   10.00   11.73   16.00   55.00
```

### Does home court advantge differ in the regular season vs the playoffs?
![plot of chunk home_crt_reg_vs_playoffs](figure/home_crt_reg_vs_playoffs-1.png)
  * *Analysis: Suprisingly the playoffs offer a stronger home court advantage despite the better teams playing each other*

### Is home court advantage diminishing over time? 
![plot of chunk home_crt_over_time](figure/home_crt_over_time-1.png)
  * *Analysis: Generally home court advantage is slightly decreasing over time. 
    However last year within 2016 there was a very strong resurgance for Home Court within the playoffs.* **Theories?**

# Total points scored Analysis
![plot of chunk total_pts](figure/total_pts-1.png)
  * *Analysis: Less points per game are scored within playoffs. 
    Likely due too diminished pace or more conservative officiating.* TODO: Can verify both hypothesis


![plot of chunk total_pts_over_time](figure/total_pts_over_time-1.png)
  * *General trajectory of the league is increasing point totals. 2011 was lockout year and explains dampened point totals*

### Which Half Scores mores points?
![plot of chunk half_analysis](figure/half_analysis-1.png)

```
## # A tibble: 2 x 2
##              half  ave_pts
##             <chr>    <dbl>
## 1  first_half_pts 99.70570
## 2 second_half_pts 97.56893
```
  * *Analysis: Within 2nd half ~ 2 less points are scored*

### What % of games go into overtime? 

```
## # A tibble: 2 x 2
##       reg_season overtime_percent
##           <fctr>            <dbl>
## 1 Regular_Season         6.209715
## 2       Playoffs         6.698113
```



