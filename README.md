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
![tree](model/img_tree.PNG)

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

| Date       |   h_course | HomeTeam       |   d_course | AwayTeam      |   a_course |   pr_h_won |   pr_draw |   pr_a_won | prediction   |
|:-----------|-----------:|:---------------|-----------:|:--------------|-----------:|-----------:|----------:|-----------:|:-------------|
| 2021-12-12 |       1.75 | Leicester      |       4    | Newcastle     |       4.4  |     0.5048 |    0.3002 |     0.195  | H            |
| 2021-12-12 |       3.65 | Burnley        |       3.6  | West Ham      |       2    |     0.1869 |    0.2506 |     0.5626 | A            |
| 2021-12-12 |       2.27 | Crystal Palace |       3.05 | Everton       |       3.3  |     0.462  |    0.3761 |     0.1619 | H            |
| 2021-12-14 |       4.8  | Brentford      |       3.9  | Man. Utd      |       1.67 |     0.3198 |    0.3798 |     0.3003 | D            |
| 2021-12-14 |       3.6  | Norwich        |       3.3  | Aston Villa   |       2.04 |     0.4418 |    0.2572 |     0.3009 | A            |
| 2021-12-14 |       1.17 | Man. City      |       7.5  | Leeds         |      16.25 |     0.7349 |    0.1361 |     0.129  | H            |
| 2021-12-15 |       2.01 | Burnley        |       3.4  | Watford       |       3.6  |     0.3401 |    0.3627 |     0.2972 | D            |
| 2021-12-15 |       2.4  | Crystal Palace |       3.25 | Southampton   |       2.95 |     0.4085 |    0.321  |     0.2705 | D            |
| 2021-12-15 |       2.04 | Brighton       |       3.15 | Wolverhampton |       3.8  |     0.3809 |    0.3163 |     0.3028 | D            |
| 2021-12-15 |       2.15 | Arsenal        |       3.45 | West Ham      |       3.2  |     0.3935 |    0.2545 |     0.352  | A            |
| 2021-12-16 |       2.1  | Leicester      |       3.5  | Tottenham     |       3.3  |     0.3138 |    0.3353 |     0.3509 | D            |
| 2021-12-16 |       1.25 | Chelsea        |       5.75 | Everton       |      13.25 |     0.7862 |    0.1583 |     0.0555 | H            |
| 2021-12-16 |       1.12 | Liverpool      |       8.75 | Newcastle     |      23.5  |     0.8471 |    0.1014 |     0.0515 | H            |

