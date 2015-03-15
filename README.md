# bball model

"I am a better investor because I am a businessman and a better businessman because I am an investor" - Warren Buffett

There are cross pollination benefits to betting on basketball that can even result in being better at basketball itself. This is nice but this is NOT the aim of this Project.  The aim of this project is very simple, it is to to gather/analyze quantitative basketball data to BEAT vegas. This is a game and Mr. Vegas is our opponent. Much of the time we will refrain from transacting with Mr. Vegas and let him be. However when he is overly emotional and irrational we will attack and attack hard.  Mr vegas evolves & adapts so he is not an easy opponent, however the goal for 2015/2016 season is to take 10K dollars from Mr vegas in side income. Otherwise he will take it from us and anything less will be considered a failure.  

Next Steps
============
First and formemost the most important step is to build a a historical database to be able to quantitatively test for edge.  We are lucky as new and creative Idea generation is a strength of the team. The reality is the execution on this backtesting framework will ultimately determine whether or not we can beat Mr. Vegas!

1)  Populate A database with ~ 10 seasons of historical data. The Key of the DB will be all of ->  Date Played, HomeTeam, AwayTeam.  All team team level statistics can be joined to this table. 

2) Join Mr. Vegas's Historical Point spreads and O/U lines. (Bonus if Halftime Data is avaiable)
  2a) Create simple Model On Macro Team Statistics 
  
Once Completed for a sanity check, we should be able to replicate simple studies such as [this](http://insider.espn.go.com/nba/story/_/id/12243076/nba-analyzing-diminishing-value-home-court-advantage). Should also be able to replicate U shpaed graph of player Productivity (by position) as a function of age. [example-graph](http://s1039.photobucket.com/user/hatch113/media/qbdeltapeak3yrsbyage.png.html)

Secondary Steps ( Micro Data) 
=================
* The above data is the team Macro Level Data. This is half the equation. Once this is completed then we will also need to gather and analyze micro or player level data. No one statistic is perfect, however if forced to use just 1 aggregate statistic to asses player value , we prefer [real plus-minus](http://espn.go.com/nba/story/_/id/10740818/introducing-real-plus-minus).  
* There are endless simple box-score and statistics and therefore It is Important to do a review of the concepts and [mathematics](http://www.basketball-reference.com/about/per.html) to determine strenghts/weaknesses and applicability.  One example is Player Efficienty Rating often marketed on ESPN. Igor Is not a fan of this statistic (criticism)[http://wagesofwins.com/2006/11/17/a-comment-on-the-player-efficiency-rating/] but this is open to debate.
* Lets do this over a weekend?

Third Steps
===============
Assuming all Macro / Micro level data has been gathered and analyzed and all ideas tested...
* Calcualte optimal betting amount, see [kelly criteria](http://en.wikipedia.org/wiki/Kelly_criterion). For now just use heuristic of more edge will generate larger bet
* Determine mathematically exact point it is preferential to bet MoneyLine vs Point Spread given Win Probablity , Win Payouts. 

Ideas To Investigate
=============
* The Point should not deviate signficiantly from point differential.  Use [SRS](http://www.basketball-reference.com/blog/?p=39) point differential to weight strength of schedule. It is believed when this Diverges > ~ 4 points (recent delta weighted higher) this alone can be slightly profitable vs Mr. Vegas.

* Home Court advantage applied unanimously to all spreads. (~2.75 pts) This is probably wrong. Home court can serve as a proxy for travel distance of away team rather than homecrowd/familiarity/etc. Therefore home-court should be broken down into distance traveled by away team.   The article above demonstrates home-court has a continuously diminished effect within recent years.  Need to validate this

* Related to above is back to back game fatigue priced into spread. Perhaphs younger teams are not as susciptible to fatigue? Minutes played weighted average of team age should be calculated to test hpothesis. Perphaphs if "fatigue" effect is present it typically doesen't materialize in first half. Therefore if this is just priced into overall spread and halftime spread is overall/2, halftime Spread is underpriced. 

* Shot Distribution of teams should be tracked. Long 2 is worst EV shot in Basketball. If offensivie effeciency deviates significantly from this number than it might not be sustainable.

* Over/Under betting will largely be a function of both team's  offensive effeciency, defensive efficiencey, pace, etc. However there are probably non - random effects the choice of referee officiating a game. This should also be tracked! (Some are more prone to call games conservatively, others liberally). 1 insteresting statistic is mavericks are 1 - 15 within playoffs when Joey Crawford officiates game. (Perhaphs noise?)


