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

| Date       |   h_odds   | HomeTeam       |   d_odds   | AwayTeam       |   a_odds   |   pr_h_won |   pr_draw |   pr_a_won | prediction   |
|:-----------|-----------:|:---------------|-----------:|:---------------|-----------:|-----------:|----------:|-----------:|:-------------|
| 2022-03-05 |       1.79 | Leicester      |       3.95 | Leeds          |       3.95 |     0.3822 |    0.3797 |     0.2381 | D            |
| 2022-03-05 |       7    | Burnley        |       4.15 | Chelsea        |       1.5  |     0.2158 |    0.2129 |     0.5714 | A            |
| 2022-03-05 |       2.9  | Norwich        |       3    | Brentford      |       2.55 |     0.4405 |    0.329  |     0.2304 | D            |
| 2022-03-05 |       2.33 | Aston Villa    |       3.3  | Southampton    |       2.95 |     0.2962 |    0.2584 |     0.4454 | A            |
| 2022-03-05 |       2.3  | Wolverhampton  |       3    | Crystal Palace |       3.35 |     0.5119 |    0.2903 |     0.1978 | H            |
| 2022-03-05 |       2.65 | Newcastle      |       3.05 | Brighton       |       2.75 |     0.4898 |    0.2935 |     0.2167 | H            |
| 2022-03-05 |       1.32 | Liverpool      |       5.65 | West Ham       |       8.65 |     0.8013 |    0.1025 |     0.0962 | H            |
| 2022-03-06 |       5.6  | Watford        |       3.9  | Arsenal        |       1.58 |     0.1582 |    0.2049 |     0.6368 | A            |
| 2022-03-06 |       1.4  | Man. City      |       4.9  | Man. Utd       |       7.35 |     0.739  |    0.1285 |     0.1325 | H            |
| 2022-03-07 |       1.62 | Tottenham      |       3.95 | Everton        |       5.15 |     0.5092 |    0.3189 |     0.1719 | H            |
| 2022-03-10 |       1.8  | Wolverhampton  |       3.45 | Watford        |       4.45 |     0.6207 |    0.2446 |     0.1347 | H            |
| 2022-03-10 |       1.88 | Southampton    |       3.55 | Newcastle      |       3.9  |     0.3589 |    0.2847 |     0.3564 | A            |
| 2022-03-10 |       2.85 | Leeds          |       3.2  | Aston Villa    |       2.46 |     0.2754 |    0.3365 |     0.3881 | D            |
| 2022-03-12 |       6.15 | Brighton       |       4.55 | Liverpool      |       1.47 |     0.1001 |    0.2167 |     0.6832 | A            |
| 2022-03-12 |       2.3  | Brentford      |       3.2  | Burnley        |       3.15 |     0.3002 |    0.2999 |     0.3999 | D            |
| 2022-03-12 |       1.9  | Man. Utd       |       3.6  | Tottenham      |       3.8  |     0.6837 |    0.1846 |     0.1317 | H            |
| 2022-03-13 |       1.33 | Chelsea        |       5.2  | Newcastle      |       8.9  |     0.4957 |    0.2274 |     0.2769 | H            |
| 2022-03-13 |       1.77 | Leeds          |       3.8  | Norwich        |       4.2  |     0.4597 |    0.3157 |     0.2246 | D            |
| 2022-03-13 |       1.99 | West Ham       |       3.45 | Aston Villa    |       3.65 |     0.5648 |    0.2755 |     0.1597 | H            |
| 2022-03-13 |       2.45 | Everton        |       3.15 | Wolverhampton  |       2.9  |     0.2903 |    0.2999 |     0.4098 | D            |
| 2022-03-13 |       1.67 | Southampton    |       3.85 | Watford        |       4.8  |     0.6292 |    0.241  |     0.1298 | H            |
| 2022-03-13 |       1.54 | Arsenal        |       4.25 | Leicester      |       5.6  |     0.5902 |    0.301  |     0.1088 | H            |
| 2022-03-14 |      10    | Crystal Palace |       5.65 | Man. City      |       1.29 |     0.1443 |    0.2148 |     0.6409 | A            |
