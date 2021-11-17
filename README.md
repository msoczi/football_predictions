## Football matches result predictions

The aim of the project was to create a tool for predicting the results of league matches from the leading European leagues based on data prepared by myself.

The project was implemented _from scratch_, i.e. it included:
- collection of raw data on the basis of which it will be possible to create characteristics and then modeling
- creating variables based on i.a. time aggregates (last n matches), position in the table, team form
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
The XGBoost model was built on a hand-prepared historical sample containing 3659 rows and 86 variables. As the objective function, `multi:softprob` was used so that the model's output was the probability of assigning observations to each of the 3 classes of match result - H (Home), A (Away), D (Draw).
<br>
These probabilities were then used to build a simple decision tree that would allow to categorize individual observations in a rule-based manner, i.e. to predict the final result with simple rules. This procedure allowed for the generalization of the results in such a way that the draw was not too rare. Below is the sheme of decision tree.
<br>
![tree](model/img_tree.png)

Forecasts **do not use bookmaker odds**. I provide them for information only.
<br>
<br>
So far, no API has been developed that allows for the ongoing tracking of progzones and their results.
<br>
However, it is possible to clone the repository and use it with python.
```sh
git clone https://github.com/msoczi/football_predictions
```
How to use ?
Run the <a href="main_script.py">main_script.py</a> from console e.g. 
```sh
python main_script.py
```
Then results will be saved to output.md file for league passed in the configuration file <a href="config.yaml">config.yaml</a>.


<br>
<br>
 
### Upcoming Premier League matches

| Date       |   h_course | HomeTeam       |   d_course | AwayTeam       |   a_course |   pr_h_won |   pr_draw |   pr_a_won | prediction   |
|:-----------|-----------:|:---------------|-----------:|:---------------|-----------:|-----------:|----------:|-----------:|:-------------|
| 2021-11-20 |       4.35 | Leicester      |       3.6  | Chelsea        |       1.79 |     0.1153 |    0.1135 |     0.7713 | A            |
| 2021-11-20 |       2.8  | Burnley        |       3.1  | Crystal Palace |       2.6  |     0.4033 |    0.2309 |     0.3658 | A            |
| 2021-11-20 |       2.45 | Aston Villa    |       3.2  | Brighton       |       2.85 |     0.4779 |    0.202  |     0.3201 | H            |
| 2021-11-20 |       3.5  | Norwich        |       3.3  | Southampton    |       2.09 |     0.3494 |    0.1436 |     0.507  | A            |
| 2021-11-20 |       2.9  | Wolverhampton  |       3.2  | West Ham       |       2.44 |     0.3581 |    0.168  |     0.4738 | A            |
| 2021-11-20 |       6.05 | Watford        |       4.4  | Man. Utd       |       1.52 |     0.3733 |    0.1913 |     0.4354 | A            |
| 2021-11-20 |       2.6  | Newcastle      |       3.2  | Brentford      |       2.7  |     0.4377 |    0.1833 |     0.379  | A            |
| 2021-11-20 |       1.5  | Liverpool      |       4.5  | Arsenal        |       6.2  |     0.711  |    0.1403 |     0.1487 | H            |
| 2021-11-21 |       1.16 | Man. City      |       7.75 | Everton        |      17    |     0.8697 |    0.088  |     0.0424 | H            |
| 2021-11-21 |       1.72 | Tottenham      |       3.9  | Leeds          |       4.35 |     0.4001 |    0.3104 |     0.2895 | D            |
| 2021-11-27 |       1.43 | Arsenal        |       4.75 | Newcastle      |       6.6  |     0.7862 |    0.1449 |     0.069  | H            |
| 2021-11-27 |       2.26 | Crystal Palace |       3.2  | Aston Villa    |       3.2  |     0.6403 |    0.2046 |     0.1551 | H            |
| 2021-11-27 |       1.3  | Liverpool      |       5.8  | Southampton    |       8.7  |     0.8308 |    0.0996 |     0.0696 | H            |
| 2021-11-27 |       3.35 | Norwich        |       3.35 | Wolverhampton  |       2.14 |     0.303  |    0.2016 |     0.4954 | A            |
| 2021-11-27 |       2.2  | Brighton       |       3.3  | Leeds          |       3.2  |     0.47   |    0.2174 |     0.3126 | H            |
| 2021-11-28 |       3.6  | Burnley        |       3.3  | Tottenham      |       2.06 |     0.6517 |    0.1645 |     0.1838 | H            |
| 2021-11-28 |       1.49 | Leicester      |       4.4  | Watford        |       6.05 |     0.5057 |    0.175  |     0.3193 | H            |
| 2021-11-28 |       2.44 | Brentford      |       3.15 | Everton        |       2.95 |     0.545  |    0.1802 |     0.2748 | H            |
| 2021-11-28 |       1.32 | Man. City      |       5.6  | West Ham       |       8.55 |     0.7265 |    0.1582 |     0.1153 | H            |
| 2021-11-28 |       1.75 | Chelsea        |       3.6  | Man. Utd       |       4.6  |     0.6719 |    0.1256 |     0.2024 | H            |
