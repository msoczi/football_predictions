## Football matches result predictions

The aim of the project was to create a tool for predicting the results of league matches from the leading European leagues based on data prepared by myself.

The project was implemented _from scratch_, i.e. it included:
- collection of raw data on the basis of which it will be possible to create characteristics and then modeling
- creating variables based on i.a. time aggregates (last n matches), position in the table, team form, betting odds
- calculate historical data for modeling
- building the target solution: XGBoost model with 3 classes. Then, based on the estimated probability, a decision tree was created, which in a simple, rule-based way predicts which team will win the match (or a possible draw)
- creating a script that downloads data about upcoming matches with bookmaker odds (www.sts.pl), creating model variables for given teams and prediction of the match result.

Raw data with match results are downloaded from https://www.football-data.co.uk. <br>
The advantage of the approach is the ability to predict results from any league. But o far, it is possible to predict the results of the first league of the following countries:
- England
- Italy
- Germany
- Spain

Based on the raw data, I created the appropriate characteristics by myself. The full list of variables is available in the file: <a href="model/variables.md">variables</a>
<br>
<br>
The XGBoost model was built on a hand-prepared historical sample containing 3659 rows and 85 variables. As the objective function, `multi: softprob` was used so that the model's output was the probability of assigning observations to each of the 3 classes of match result - H (Home), A (Away), D (Draw).
<br>
These probabilities were then used to build a simple decision tree that would allow to categorize individual observations in a rule-based manner, i.e. to predict the final result with simple rules. This procedure allowed for the generalization of the results in such a way that the draw was not too rare (that was a problem - the draw practically did not occur). Below is the sheme of decision tree.
<br>
![tree](model/img_tree.png)

The forecasts are made on the basis of scraping information about the upcoming matches from the website www.sts.pl.
<br>
<br>
So far, no API has been developed that allows for the ongoing tracking of progzones and their results.
<br>
However, it is possible to clone the repository and use it with python.
```sh
git clone https://github.com/msoczi/football_predictions
```
You can use the package in two ways:
1. Interactive - via Jupyter Notebook - as the main function argument pass the name of the league for which you want to get forecasts. 
2. Run the <a href="main_script.py">main_script.py</a> from console e.g. 
```sh
python main_script.py
```
Then results will be saved to output.md file for league passed in the configuration file <a href="config.yaml">config.yaml</a>.


<br>
<br>
 
### Upcoming Premier League matches


|  Date        |  HomeTeam          |  AwayTeam          |  pr_h_won  |     pr_draw  |  pr_a_won  |  prediction  |  result  |
|:------------:|--------------------|--------------------|------------|--------------|------------|:------------:|:--------:|
|  2021-09-11  |  Crystal Palace    |  Tottenham         | 0.329318   | 0.326657     | 0.344026   | A            | H        |
|  2021-09-11  |  Man. Utd          |  Newcastle         | 0.377006   | 0.313049     | 0.309945   | H            | H        |
|  2021-09-11  |  Brentford         |  Brighton          | 0.334466   | 0.328736     | 0.336798   | D            | A        |
|  2021-09-11  |  Watford           |  Wolverhampton     | 0.333558   | 0.328423     | 0.338019   | D            | A        |
|  2021-09-11  |  Arsenal           |  Norwich           | 0.361551   | 0.32278      | 0.315669   | H            | H        |
|  2021-09-11  |  Southampton       |  West Ham          | 0.332461   | 0.324929     | 0.34261    | A            | D        |
|  2021-09-11  |  Leicester         |  Man. City         | 0.316791   | 0.322214     | 0.360995   | A            | A        |
|  2021-09-11  |  Chelsea           |  Aston Villa       | 0.377019   | 0.313615     | 0.309366   | H            | H        |
|  2021-09-12  |  Leeds             |  Liverpool         | 0.322159   | 0.327243     | 0.350598   | A            | A        |
|  2021-09-13  |  Everton           |  Burnley           | 0.363973   | 0.324074     | 0.311952   | H            | H        |
|  2021-09-17  |  Newcastle         |  Leeds             | 0.335699   | 0.326577     | 0.337723   | A            | D        |
|  2021-09-18  |  Wolverhampton     |  Brentford         | 0.349846   | 0.328648     | 0.321506   | H            | A        |
|  2021-09-18  |  Burnley           |  Arsenal           | 0.331997   | 0.325836     | 0.342167   | A            | A        |
|  2021-09-18  |  Liverpool         |  Crystal Palace    | 0.375659   | 0.313657     | 0.310685   | H            | H        |
|  2021-09-18  |  Man. City         |  Southampton       | 0.381051   | 0.310775     | 0.308174   | H            | D        |
|  2021-09-18  |  Norwich           |  Watford           | 0.344787   | 0.327089     | 0.328124   | A            | A        |
|  2021-09-18  |  Aston Villa       |  Everton           | 0.332298   | 0.330005     | 0.337697   | D            | H        |
|  2021-09-19  |  West Ham          |  Man. Utd          | 0.3324     | 0.32487      | 0.342731   | A            | A        |
|  2021-09-19  |  Brighton          |  Leicester         | 0.33882    | 0.328372     | 0.332808   | D            | H        |
|  2021-09-19  |  Tottenham         |  Chelsea           | 0.331063   | 0.326115     | 0.342822   | A            | A        |
|  2021-09-25  |  Man. Utd          |  Aston Villa       | 0.378278   | 0.313523     | 0.308199   | H            |          |
|  2021-09-25  |  Chelsea           |  Man. City         | 0.336883   | 0.325964     | 0.337154   | A            |          |
|  2021-09-25  |  Leeds             |  West Ham          | 0.334168   | 0.327476     | 0.338356   | D            |          |
|  2021-09-25  |  Watford           |  Newcastle         | 0.344243   | 0.325243     | 0.330514   | A            |          |
|  2021-09-25  |  Leicester         |  Burnley           | 0.356449   | 0.328845     | 0.314706   | H            |          |
|  2021-09-25  |  Everton           |  Norwich           | 0.364136   | 0.324724     | 0.311139   | H            |          |
|  2021-09-25  |  Brentford         |  Liverpool         | 0.315546   | 0.32133      | 0.363124   | A            |          |
|  2021-09-26  |  Southampton       |  Wolverhampton     | 0.33526    | 0.329779     | 0.334961   | D            |          |
|  2021-09-26  |  Arsenal           |  Tottenham         | 0.338959   | 0.328844     | 0.332198   | D            |          |
|  2021-09-27  |  Crystal Palace    |  Brighton          | 0.331538   | 0.327436     | 0.341026   | A            |          |
|  2021-10-02  |  Man. Utd          |  Everton           | 0.376928   | 0.313447     | 0.309624   | H            |          |
|  2021-10-02  |  Chelsea           |  Southampton       | 0.376246   | 0.314011     | 0.309743   | H            |          |
|  2021-10-02  |  Leeds             |  Watford           | 0.354046   | 0.329093     | 0.316861   | H            |          |
|  2021-10-02  |  Wolverhampton     |  Newcastle         | 0.357281   | 0.327311     | 0.315408   | H            |          |
|  2021-10-02  |  Burnley           |  Norwich           | 0.347019   | 0.325969     | 0.327012   | H            |          |
|  2021-10-02  |  Brighton          |  Arsenal           | 0.338758   | 0.328054     | 0.333188   | D            |          |
|  2021-10-03  |  West Ham          |  Brentford         | 0.35972    | 0.326228     | 0.314052   | H            |          |
|  2021-10-03  |  Tottenham         |  Aston Villa       | 0.346609   | 0.331328     | 0.322063   | D            |          |
|  2021-10-03  |  Crystal Palace    |  Leicester         | 0.333368   | 0.327622     | 0.33901    | D            |          |
|  2021-10-03  |  Liverpool         |  Man. City         | 0.337678   | 0.324979     | 0.337343   | A            |          |
