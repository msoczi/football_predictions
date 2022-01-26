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
| 2022-02-05 |       2.2  | Burnley       |       3.1  | Watford        |       3.45 |     0.4286 |    0.3213 |     0.25   | D            |
| 2022-02-08 |       1.42 | West Ham      |       4.85 | Watford        |       6.6  |     0.6404 |    0.2264 |     0.1332 | H            |
| 2022-02-08 |       2.55 | Newcastle     |       3.25 | Everton        |       2.7  |     0.3749 |    0.3786 |     0.2465 | D            |
| 2022-02-08 |       5.7  | Burnley       |       4    | Man. Utd       |       1.56 |     0.2555 |    0.2306 |     0.5139 | A            |
| 2022-02-09 |       3.35 | Norwich       |       3.3  | Crystal Palace |       2.14 |     0.3714 |    0.306  |     0.3226 | D            |
| 2022-02-09 |       1.13 | Man. City     |       9    | Brentford      |      19.25 |     0.8223 |    0.1241 |     0.0536 | H            |
| 2022-02-09 |       1.64 | Tottenham     |       3.9  | Southampton    |       4.95 |     0.6625 |    0.1895 |     0.148  | H            |
| 2022-02-09 |       1.96 | Aston Villa   |       3.55 | Leeds          |       3.6  |     0.5679 |    0.2735 |     0.1586 | H            |
| 2022-02-10 |       1.28 | Liverpool     |       6.1  | Leicester      |       9.1  |     0.8034 |    0.1357 |     0.0609 | H            |
| 2022-02-10 |       3.35 | Wolverhampton |       3.2  | Arsenal        |       2.19 |     0.2597 |    0.2267 |     0.5136 | A            |
| 2022-02-12 |       1.52 | Man. Utd      |       4.3  | Southampton    |       5.7  |     0.6045 |    0.2023 |     0.1932 | H            |
| 2022-02-12 |       2.6  | Brentford     |       3.05 | Crystal Palace |       2.85 |     0.2925 |    0.3454 |     0.3621 | D            |
| 2022-02-12 |       2.3  | Everton       |       3.3  | Leeds          |       3    |     0.441  |    0.3357 |     0.2233 | D            |
| 2022-02-12 |       3.4  | Watford       |       3.2  | Brighton       |       2.17 |     0.2255 |    0.286  |     0.4885 | A            |
| 2022-02-12 |      15    | Norwich       |       7.35 | Man. City      |       1.18 |     0.0917 |    0.1377 |     0.7707 | A            |
| 2022-02-13 |       1.77 | Tottenham     |       3.5  | Wolverhampton  |       4.55 |     0.626  |    0.1946 |     0.1794 | H            |
| 2022-02-13 |       8.05 | Burnley       |       4.95 | Liverpool      |       1.37 |     0.0747 |    0.1795 |     0.7458 | A            |
| 2022-02-13 |       3.05 | Newcastle     |       3.3  | Aston Villa    |       2.3  |     0.3425 |    0.321  |     0.3365 | D            |
| 2022-02-13 |       2.8  | Leicester     |       3.35 | West Ham       |       2.42 |     0.3033 |    0.2785 |     0.4182 | A            |
