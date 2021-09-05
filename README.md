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

| Date       |   h_course | HomeTeam       |   d_course | AwayTeam       |   a_course |   pr_h_won |   pr_draw |   pr_a_won | prediction   |
|:-----------|-----------:|:---------------|-----------:|:---------------|-----------:|-----------:|----------:|-----------:|:-------------|
| 2021-09-11 |       4.3  | Crystal Palace |       3.4  | Tottenham      |       1.85 |   0.329318 |  0.326657 |   0.344026 | A            |
| 2021-09-11 |       1.2  | Man. Utd       |       6.75 | Newcastle      |      14.5  |   0.377006 |  0.313049 |   0.309945 | H            |
| 2021-09-11 |       2.7  | Brentford      |       3    | Brighton       |       2.7  |   0.334466 |  0.328736 |   0.336798 | D            |
| 2021-09-11 |       3.3  | Watford        |       3.1  | Wolverhampton  |       2.24 |   0.333558 |  0.328423 |   0.338019 | D            |
| 2021-09-11 |       1.51 | Arsenal        |       4.35 | Norwich        |       5.75 |   0.361551 |  0.32278  |   0.315669 | H            |
| 2021-09-11 |       2.95 | Southampton    |       3.4  | West Ham       |       2.31 |   0.332461 |  0.324929 |   0.34261  | A            |
| 2021-09-11 |       5.5  | Leicester      |       4.15 | Man. City      |       1.55 |   0.316791 |  0.322214 |   0.360995 | A            |
| 2021-09-11 |       1.31 | Chelsea        |       5.2  | Aston Villa    |      10    |   0.377019 |  0.313615 |   0.309366 | H            |
| 2021-09-12 |       4.5  | Leeds          |       4.1  | Liverpool      |       1.67 |   0.322159 |  0.327243 |   0.350598 | A            |
| 2021-09-13 |       1.75 | Everton        |       3.6  | Burnley        |       4.6  |   0.356084 |  0.3259   |   0.318016 | H            |
| 2021-09-17 |       3.2  | Newcastle      |       3.7  | Leeds          |       2.06 |   0.334564 |  0.325473 |   0.339963 | A            |
| 2021-09-18 |       2.09 | Wolverhampton  |       3.1  | Brentford      |       3.75 |   0.342533 |  0.327754 |   0.329713 | D            |
| 2021-09-18 |       3.55 | Burnley        |       3.2  | Arsenal        |       2.12 |   0.335372 |  0.325772 |   0.338856 | A            |
| 2021-09-18 |       1.2  | Liverpool      |       7    | Crystal Palace |      13.25 |   0.37847  |  0.312406 |   0.309124 | H            |
| 2021-09-18 |       1.15 | Man. City      |       8.05 | Southampton    |      16.25 |   0.379905 |  0.31135  |   0.308745 | H            |
| 2021-09-18 |       2.11 | Norwich        |       3.4  | Watford        |       3.3  |   0.343969 |  0.326897 |   0.329134 | A            |
| 2021-09-18 |       2.55 | Aston Villa    |       3.25 | Everton        |       2.7  |   0.332302 |  0.330745 |   0.336954 | D            |
| 2021-09-19 |       3.45 | West Ham       |       3.65 | Man. Utd       |       1.99 |   0.333382 |  0.325188 |   0.34143  | A            |
| 2021-09-19 |       2.75 | Brighton       |       3.2  | Leicester      |       2.55 |   0.337163 |  0.328739 |   0.334098 | D            |
| 2021-09-19 |       3.7  | Tottenham      |       3.4  | Chelsea        |       1.98 |   0.333363 |  0.326208 |   0.340429 | A            |
