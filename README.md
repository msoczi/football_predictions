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
| 2022-01-11 |       1.96 | Southampton    |       3.45 | Brentford      |       3.75 |     0.3841 |    0.3002 |     0.3158 | D            |
| 2022-01-11 |       2.55 | Everton        |       3.35 | Leicester      |       2.65 |     0.3397 |    0.3604 |     0.2999 | D            |
| 2022-01-12 |       1.27 | West Ham       |       5.7  | Norwich        |      11.25 |     0.6766 |    0.2085 |     0.1149 | H            |
| 2022-01-14 |       2.07 | Brighton       |       3.2  | Crystal Palace |       3.7  |     0.4684 |    0.3129 |     0.2187 | H            |
| 2022-01-15 |       1.63 | Man. City      |       3.95 | Chelsea        |       5    |     0.5963 |    0.2168 |     0.1869 | H            |
| 2022-01-15 |       2.95 | Burnley        |       3.35 | Leicester      |       2.33 |     0.2898 |    0.3036 |     0.4066 | D            |
| 2022-01-15 |       2.07 | Newcastle      |       3.55 | Watford        |       3.3  |     0.3937 |    0.3239 |     0.2824 | D            |
| 2022-01-15 |       3.5  | Norwich        |       3.3  | Everton        |       2.07 |     0.2956 |    0.2743 |     0.4301 | A            |
| 2022-01-15 |       2.2  | Wolverhampton  |       3.2  | Southampton    |       3.35 |     0.4078 |    0.3431 |     0.2491 | D            |
| 2022-01-15 |       3.55 | Aston Villa    |       3.6  | Man. Utd       |       1.98 |     0.2769 |    0.2339 |     0.4892 | A            |
| 2022-01-16 |       1.36 | Liverpool      |       5.05 | Brentford      |       8.1  |     0.8212 |    0.099  |     0.0798 | H            |
| 2022-01-16 |       1.69 | West Ham       |       4    | Leeds          |       4.5  |     0.595  |    0.2843 |     0.1208 | H            |
| 2022-01-16 |       2.44 | Tottenham      |       3.25 | Arsenal        |       2.85 |     0.5266 |    0.1961 |     0.2773 | H            |
| 2022-01-21 |       2.09 | Watford        |       3.4  | Norwich        |       3.4  |     0.3297 |    0.3308 |     0.3395 | D            |
| 2022-01-22 |       2.47 | Everton        |       3.2  | Aston Villa    |       2.85 |     0.4419 |    0.2892 |     0.2689 | A            |
| 2022-01-22 |       1.53 | Arsenal        |       4.2  | Burnley        |       5.8  |     0.779  |    0.1516 |     0.0693 | H            |
| 2022-01-22 |       2.8  | Brentford      |       3.1  | Wolverhampton  |       2.55 |     0.5495 |    0.2903 |     0.1603 | H            |
| 2022-01-22 |       2.02 | Leeds          |       3.55 | Newcastle      |       3.45 |     0.4746 |    0.2978 |     0.2277 | H            |
| 2022-01-22 |       1.84 | Man. Utd       |       3.7  | West Ham       |       3.9  |     0.5026 |    0.2069 |     0.2905 | H            |
| 2022-01-22 |       8.65 | Southampton    |       5.45 | Man. City      |       1.32 |     0.0879 |    0.1862 |     0.7259 | A            |
| 2022-01-23 |       2.28 | Leicester      |       3.25 | Brighton       |       3.15 |     0.3092 |    0.271  |     0.4198 | A            |
| 2022-01-23 |       5.4  | Crystal Palace |       4.2  | Liverpool      |       1.56 |     0.1422 |    0.2487 |     0.6091 | A            |
| 2022-01-23 |       1.9  | Chelsea        |       3.6  | Tottenham      |       4.05 |     0.5749 |    0.1939 |     0.2312 | H            |
