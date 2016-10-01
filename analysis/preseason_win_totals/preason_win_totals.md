---
title:"PreaSeaon Win Projections"
output:
  md_document
---





# Forecasting presason win totals
### Naive Extrapolation
![plot of chunk naive_extrapolation](figure/naive_extrapolation-1.png)

```
## 
## Call:
## lm(formula = num_wins ~ point_diff_lag1 + point_diff_lag2)
## 
## Residuals:
##     Min      1Q  Median      3Q     Max 
## -35.002  -8.317  -0.270   9.123  37.221 
## 
## Coefficients:
##                 Estimate Std. Error t value Pr(>|t|)    
## (Intercept)     38.78272    0.66521  58.302  < 2e-16 ***
## point_diff_lag1  1.44643    0.17305   8.358 2.46e-15 ***
## point_diff_lag2 -0.03205    0.17342  -0.185    0.853    
## ---
## Signif. codes:  0 '***' 0.001 '**' 0.01 '*' 0.05 '.' 0.1 ' ' 1
## 
## Residual standard error: 11.51 on 298 degrees of freedom
##   (2 observations deleted due to missingness)
## Multiple R-squared:  0.2495,	Adjusted R-squared:  0.2445 
## F-statistic: 49.54 on 2 and 298 DF,  p-value: < 2.2e-16
```
# [Preason Trades and Age related Adjustemnt](https://docs.google.com/spreadsheets/d/1KlFDXkmHwKxIPSFrXhYxQhveo3OlG1L2_NyB7YHgk8s/edit#gid=0)
