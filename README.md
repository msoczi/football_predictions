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
| 2021-12-15 |       2.2  | Crystal Palace |       3.25 | Southampton    |       3.45 |     0.4247 |    0.313  |     0.2622 | D            |
| 2021-12-15 |       2.55 | Brighton       |       2.9  | Wolverhampton  |       3.2  |     0.4512 |    0.3294 |     0.2194 | D            |
| 2021-12-15 |       2.15 | Arsenal        |       3.6  | West Ham       |       3.25 |     0.4585 |    0.2249 |     0.3166 | A            |
| 2021-12-16 |       2.25 | Leicester      |       3.7  | Tottenham      |       3    |     0.4028 |    0.3074 |     0.2899 | D            |
| 2021-12-16 |       1.23 | Chelsea        |       6.25 | Everton        |      13    |     0.7629 |    0.1599 |     0.0772 | H            |
| 2021-12-16 |       1.13 | Liverpool      |       8.75 | Newcastle      |      19.75 |     0.829  |    0.1133 |     0.0576 | H            |
| 2021-12-18 |       1.53 | Man. Utd       |       4.2  | Brighton       |       5.7  |     0.5364 |    0.2391 |     0.2245 | H            |
| 2021-12-18 |       3    | Watford        |       3.3  | Crystal Palace |       2.32 |     0.275  |    0.3117 |     0.4133 | D            |
| 2021-12-18 |       2.05 | Southampton    |       3.4  | Brentford      |       3.5  |     0.4954 |    0.2859 |     0.2187 | H            |
| 2021-12-18 |       1.36 | West Ham       |       4.95 | Norwich        |       8.25 |     0.6377 |    0.2203 |     0.142  | H            |
| 2021-12-18 |       1.75 | Aston Villa    |       3.7  | Burnley        |       4.45 |     0.4634 |    0.3227 |     0.2139 | H            |
| 2021-12-18 |       3.2  | Leeds          |       3.5  | Arsenal        |       2.13 |     0.3915 |    0.2358 |     0.3728 | A            |
| 2021-12-19 |       2.85 | Everton        |       3.2  | Leicester      |       2.48 |     0.3788 |    0.2579 |     0.3633 | A            |
| 2021-12-19 |       5.95 | Wolverhampton  |       4    | Chelsea        |       1.54 |     0.1004 |    0.1985 |     0.7011 | A            |
| 2021-12-19 |      13    | Newcastle      |       6.25 | Man. City      |       1.23 |     0.0946 |    0.16   |     0.7454 | A            |
| 2021-12-19 |       4.8  | Tottenham      |       4.1  | Liverpool      |       1.63 |     0.2374 |    0.2243 |     0.5384 | A            |

