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
| 2022-02-19 |       1.68 | West Ham       |       3.9  | Newcastle      |       4.65 |     0.5567 |    0.2629 |     0.1804 | H            |
| 2022-02-19 |       1.72 | Brighton       |       3.5  | Burnley        |       4.95 |     0.6643 |    0.214  |     0.1217 | H            |
| 2022-02-19 |       1.45 | Arsenal        |       4.35 | Brentford      |       6.9  |     0.7343 |    0.1671 |     0.0985 | H            |
| 2022-02-19 |       5.05 | Crystal Palace |       3.75 | Chelsea        |       1.66 |     0.2059 |    0.2431 |     0.551  | A            |
| 2022-02-19 |       1.12 | Liverpool      |       8.75 | Norwich        |      23.5  |     0.8763 |    0.0819 |     0.0418 | H            |
| 2022-02-19 |       1.61 | Aston Villa    |       3.9  | Watford        |       5.25 |     0.5193 |    0.2901 |     0.1907 | H            |
| 2022-02-19 |       2.07 | Southampton    |       3.45 | Everton        |       3.4  |     0.5022 |    0.2835 |     0.2144 | H            |
| 2022-02-19 |       1.27 | Man. City      |       5.75 | Tottenham      |      10.5  |     0.7042 |    0.1826 |     0.1131 | H            |
| 2022-02-20 |       3.8  | Leeds          |       3.7  | Man. Utd       |       1.88 |     0.2797 |    0.1651 |     0.5552 | A            |
| 2022-02-20 |       2.3  | Wolverhampton  |       3.15 | Leicester      |       3.15 |     0.4867 |    0.3375 |     0.1759 | H            |
| 2022-02-23 |       4    | Burnley        |       3.35 | Tottenham      |       1.92 |     0.1851 |    0.2566 |     0.5583 | A            |
| 2022-02-23 |       3.35 | Watford        |       3.15 | Crystal Palace |       2.21 |     0.3106 |    0.2995 |     0.3899 | D            |
| 2022-02-23 |       1.18 | Liverpool      |       7.6  | Leeds          |      13.75 |     0.7951 |    0.146  |     0.0589 | H            |
| 2022-02-24 |       1.64 | Arsenal        |       3.65 | Wolverhampton  |       5.45 |     0.6284 |    0.1668 |     0.2048 | H            |
| 2022-02-25 |       1.65 | Southampton    |       3.9  | Norwich        |       4.9  |     0.6842 |    0.1921 |     0.1237 | H            |
| 2022-02-26 |       3.4  | Leeds          |       3.4  | Tottenham      |       2.09 |     0.2727 |    0.2441 |     0.4832 | A            |
| 2022-02-26 |       2.38 | Brentford      |       3.25 | Newcastle      |       2.95 |     0.248  |    0.375  |     0.377  | D            |
| 2022-02-26 |       1.33 | Man. Utd       |       5.2  | Watford        |       8.75 |     0.647  |    0.2043 |     0.1487 | H            |
| 2022-02-26 |       1.89 | Crystal Palace |       3.4  | Burnley        |       4.05 |     0.5592 |    0.2589 |     0.182  | H            |
| 2022-02-26 |       2.36 | Brighton       |       3.15 | Aston Villa    |       3.05 |     0.535  |    0.2519 |     0.2131 | H            |
| 2022-02-26 |      10    | Everton        |       5.7  | Man. City      |       1.28 |     0.1287 |    0.1594 |     0.7119 | A            |
| 2022-02-27 |       1.96 | West Ham       |       3.35 | Wolverhampton  |       3.85 |     0.4957 |    0.2557 |     0.2486 | H            |
| 2022-03-01 |       3.2  | Burnley        |       3.3  | Leicester      |       2.21 |     0.3376 |    0.3627 |     0.2997 | D            |
