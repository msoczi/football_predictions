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

| Date       |   h_course | HomeTeam       |   d_course | AwayTeam       |   a_course |   pr_h_won |   pr_draw |   pr_a_won | prediction   |
|:-----------|-----------:|:---------------|-----------:|:---------------|-----------:|-----------:|----------:|-----------:|:-------------|
| 2021-11-27 |       1.47 | Arsenal        |       4.6  | Newcastle      |       6    |     0.6604 |    0.2298 |     0.1098 | H            |
| 2021-11-27 |       2.19 | Crystal Palace |       3.2  | Aston Villa    |       3.3  |     0.5286 |    0.2725 |     0.1988 | H            |
| 2021-11-27 |       1.27 | Liverpool      |       6.25 | Southampton    |       9.75 |     0.7834 |    0.1258 |     0.0908 | H            |
| 2021-11-27 |       3.35 | Norwich        |       3.25 | Wolverhampton  |       2.15 |     0.2532 |    0.2412 |     0.5056 | A            |
| 2021-11-27 |       2.08 | Brighton       |       3.35 | Leeds          |       3.45 |     0.3364 |    0.3224 |     0.3412 | D            |
| 2021-11-28 |       3.7  | Burnley        |       3.45 | Tottenham      |       1.97 |     0.445  |    0.3048 |     0.2503 | D            |
| 2021-11-28 |       1.6  | Leicester      |       4.1  | Watford        |       5.05 |     0.4748 |    0.2939 |     0.2314 | H            |
| 2021-11-28 |       2.3  | Brentford      |       3.15 | Everton        |       3.15 |     0.4783 |    0.2857 |     0.236  | H            |
| 2021-11-28 |       1.32 | Man. City      |       5.5  | West Ham       |       8.6  |     0.7126 |    0.1379 |     0.1495 | H            |
| 2021-11-28 |       1.58 | Chelsea        |       3.95 | Man. Utd       |       5.55 |     0.6862 |    0.1874 |     0.1265 | H            |
| 2021-11-30 |       1.95 | Newcastle      |       3.5  | Norwich        |       3.7  |     0.4974 |    0.2678 |     0.2348 | H            |
| 2021-11-30 |       2.35 | Leeds          |       3.25 | Crystal Palace |       3    |     0.3636 |    0.2661 |     0.3703 | A            |
| 2021-12-01 |       2.6  | Southampton    |       3.3  | Leicester      |       2.65 |     0.4899 |    0.2568 |     0.2533 | H            |
| 2021-12-01 |       1.94 | Wolverhampton  |       3.3  | Burnley        |       3.95 |     0.5924 |    0.2859 |     0.1218 | H            |
| 2021-12-01 |       2.07 | West Ham       |       3.35 | Brighton       |       3.5  |     0.5977 |    0.2346 |     0.1677 | H            |
| 2021-12-01 |       8    | Watford        |       4.8  | Chelsea        |       1.38 |     0.0961 |    0.1694 |     0.7344 | A            |
| 2021-12-01 |       7.6  | Aston Villa    |       5    | Man. City      |       1.38 |     0.0902 |    0.173  |     0.7367 | A            |
| 2021-12-01 |       5.4  | Everton        |       4.5  | Liverpool      |       1.52 |     0.1306 |    0.1883 |     0.681  | A            |
| 2021-12-02 |       1.64 | Tottenham      |       3.85 | Brentford      |       5.15 |     0.4434 |    0.3123 |     0.2442 | D            |
| 2021-12-02 |       2.14 | Man. Utd       |       3.4  | Arsenal        |       3.3  |     0.2361 |    0.3256 |     0.4383 | D            |

