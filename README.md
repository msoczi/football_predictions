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
| 2021-12-26 |       1.86 | Wolverhampton  |       3.45 | Watford        |       4.15 |     0.3959 |    0.374  |     0.2301 | D            |
| 2021-12-26 |       1.18 | Liverpool      |       7.5  | Leeds          |      14.5  |     0.8468 |    0.1094 |     0.0438 | H            |
| 2021-12-26 |       1.74 | Tottenham      |       3.65 | Crystal Palace |       4.55 |     0.6151 |    0.2263 |     0.1586 | H            |
| 2021-12-26 |       2.48 | Burnley        |       3.05 | Everton        |       2.95 |     0.4075 |    0.3375 |     0.255  | D            |
| 2021-12-26 |       6.4  | Norwich        |       4.4  | Arsenal        |       1.47 |     0.2836 |    0.1714 |     0.545  | A            |
| 2021-12-26 |       1.76 | West Ham       |       3.8  | Southampton    |       4.25 |     0.513  |    0.2568 |     0.2302 | H            |
| 2021-12-26 |       1.21 | Man. City      |       6.7  | Leicester      |      12.5  |     0.819  |    0.11   |     0.0711 | H            |
| 2021-12-26 |       5.15 | Aston Villa    |       3.75 | Chelsea        |       1.65 |     0.1687 |    0.1983 |     0.6329 | A            |
| 2021-12-26 |       1.92 | Brighton       |       3.35 | Brentford      |       4.05 |     0.4605 |    0.3317 |     0.2078 | D            |
| 2021-12-27 |       5.95 | Newcastle      |       4.55 | Man. Utd       |       1.48 |     0.2725 |    0.2256 |     0.5019 | A            |
| 2021-12-28 |       1.71 | Arsenal        |       3.65 | Wolverhampton  |       4.8  |     0.7363 |    0.165  |     0.0987 | H            |
| 2021-12-28 |       1.65 | Crystal Palace |       3.8  | Norwich        |       5.05 |     0.5541 |    0.2855 |     0.1605 | H            |
| 2021-12-28 |       3.5  | Watford        |       3.5  | West Ham       |       2    |     0.3079 |    0.244  |     0.4481 | A            |
| 2021-12-28 |       3.1  | Southampton    |       3.35 | Tottenham      |       2.23 |     0.2936 |    0.3174 |     0.3891 | D            |
| 2021-12-28 |       2.8  | Leeds          |       3.2  | Aston Villa    |       2.5  |     0.2754 |    0.3283 |     0.3963 | D            |
| 2021-12-28 |       5.15 | Leicester      |       4.2  | Liverpool      |       1.58 |     0.1636 |    0.1975 |     0.6389 | A            |
| 2021-12-29 |       1.39 | Chelsea        |       4.6  | Brighton       |       7.8  |     0.7752 |    0.137  |     0.0879 | H            |
| 2021-12-29 |      12.5  | Brentford      |       6.15 | Man. City      |       1.23 |     0.1081 |    0.1784 |     0.7135 | A            |
| 2021-12-30 |       1.86 | Everton        |       3.55 | Newcastle      |       4.05 |     0.492  |    0.3529 |     0.1552 | H            |
| 2021-12-30 |       1.35 | Man. Utd       |       5.1  | Burnley        |       8.25 |     0.5804 |    0.2695 |     0.1501 | H            |
