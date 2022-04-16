## Football matches result predictions

The aim of the project was to create a tool for predicting the results of league matches from the leading European leagues based on data prepared by myself.

The project was implemented _from scratch_, i.e. it included:
- collection of raw data on the basis of which it will be possible to create characteristics and then modeling
- creating variables based on i.a. time aggregates (last n matches), position in the table, team form, etc.
- calculate historical data for modeling
- building the target solution: XGBoost model with 3 classes. Then, based on the estimated probability, a decision tree was created, which in a simple, rule-based way predicts which team will win the match (or a possible draw)
- creating a script that downloads data about upcoming matches with bookmaker odds (www.sts.pl), creating model variables for given teams and prediction of the match result.

Raw data with match results are downloaded from https://www.football-data.co.uk. <br>
The advantage of the approach is the ability to predict results from any league. But o far, it is possible to predict the results of the first league of the following countries:
- England
- Italy
- Germany
- Spain
- France

Based on the raw data, I created the appropriate characteristics by myself. The full list of variables is available in the file: <a href="model/variables.md">variables</a>
<br>
<br>
The XGBoost model was built on a hand-prepared historical sample containing 7210 rows and 354 columns. As the objective function, `multi:softprob` was used so that the model's output was the probability of assigning observations to each of the 3 classes of match result - **H (Home), A (Away), D (Draw)**.
<br>
These probabilities were then used to build a simple decision tree (`max_depth = 3`) that would allow to categorize individual observations in a rule-based manner, i.e. to predict the final result with simple rules. This procedure allowed for the generalization of the results in such a way that the draw was not too rare. Below is the sheme of decision tree.
<br>
![tree](model/img_tree.PNG)

Forecasts **do not use bookmaker odds**. I provide them for information only.
<br>
<br>
So far, no API has been developed that allows for the online forecasting.
<br>
However, it is possible to clone the repository and use it with python.
<br>
How to use?
1. Clone repository.
```sh
git clone https://github.com/msoczi/football_predictions
```
2. Create and activate virtual environment for python.
```sh
# LINUX:
python3 -m venv football_preds
source football_preds/bin/activate

# WINDOWS:
python -m venv football_preds
football_preds/Scripts/activate
```
3. Install required packages (in virtual environment!).
```sh
pip install -r requirements.txt
```
4. Run the <a href="main_script.py">main_script.py</a> from console.
```sh
python main_script.py
```
Then results will be saved to output.md file for league passed in the configuration file <a href="config.yaml">config.yaml</a>.

<br>
 
### Upcoming Premier League matches

|    Date    |  H - odds  | HomeTeam       |  D - odds  | AwayTeam       |  A - odds  | prob H win | prob draw | prob A win |  Prediction  |
|:-----------|-----------:|:---------------|-----------:|:---------------|-----------:|-----------:|----------:|-----------:|:-------------|
| 2022-04-16 |       1.55 | Tottenham      |       4.15 | Brighton       |       6.1  |     0.6036 |    0.1954 |     0.201  | H            |
| 2022-04-16 |       2.85 | Watford        |       3.15 | Brentford      |       2.5  |     0.3377 |    0.272  |     0.3903 | D            |
| 2022-04-16 |       3.75 | Southampton    |       3.5  | Arsenal        |       1.94 |     0.2933 |    0.2038 |     0.5029 | A            |
| 2022-04-16 |       1.25 | Man. Utd       |       6.25 | Norwich        |      11    |     0.66   |    0.2024 |     0.1376 | H            |
| 2022-04-17 |       1.7  | West Ham       |       3.7  | Burnley        |       4.75 |     0.6646 |    0.1786 |     0.1567 | H            |
| 2022-04-17 |       2.22 | Newcastle      |       3.25 | Leicester      |       3.2  |     0.3688 |    0.2243 |     0.4069 | A            |
| 2022-04-19 |       1.46 | Liverpool      |       4.65 | Man. Utd       |       6.15 |     0.618  |    0.1793 |     0.2027 | H            |
| 2022-04-20 |       2.45 | Newcastle      |       3.15 | Crystal Palace |       2.9  |     0.4097 |    0.2445 |     0.3458 | A            |
| 2022-04-20 |       2.44 | Everton        |       3.25 | Leicester      |       2.85 |     0.3125 |    0.2297 |     0.4578 | A            |
| 2022-04-20 |       2.01 | Chelsea        |       3.35 | Arsenal        |       3.65 |     0.5619 |    0.1957 |     0.2424 | H            |
| 2022-04-20 |       1.18 | Man. City      |       7.15 | Brighton       |      16    |     0.7321 |    0.1591 |     0.1088 | H            |
| 2022-04-21 |       2.9  | Burnley        |       3.2  | Southampton    |       2.44 |     0.3289 |    0.2691 |     0.402  | D            |
| 2022-04-23 |       2.24 | Arsenal        |       3.3  | Man. Utd       |       3.1  |     0.5298 |    0.2089 |     0.2613 | H            |
| 2022-04-23 |       2.65 | Leicester      |       3.3  | Aston Villa    |       2.6  |     0.4685 |    0.2683 |     0.2632 | H            |
| 2022-04-23 |       3.6  | Norwich        |       3.3  | Newcastle      |       2.05 |     0.2844 |    0.2902 |     0.4254 | D            |
| 2022-04-23 |       1.1  | Man. City      |       9.95 | Watford        |      24    |     0.7677 |    0.1514 |     0.0809 | H            |
| 2022-04-23 |       3.85 | Brentford      |       3.45 | Tottenham      |       1.93 |     0.2861 |    0.1879 |     0.526  | A            |
| 2022-04-24 |       1.57 | Chelsea        |       4.05 | West Ham       |       5.45 |     0.7153 |    0.1537 |     0.1309 | H            |
| 2022-04-24 |       2.75 | Burnley        |       2.95 | Wolverhampton  |       2.75 |     0.3219 |    0.3261 |     0.3521 | D            |
| 2022-04-24 |       2.22 | Brighton       |       3.25 | Southampton    |       3.25 |     0.4281 |    0.2785 |     0.2934 | D            |
| 2022-04-24 |       1.21 | Liverpool      |       6.8  | Everton        |      13    |     0.7678 |    0.1412 |     0.091  | H            |
| 2022-04-25 |       2.08 | Crystal Palace |       3.35 | Leeds          |       3.45 |     0.4836 |    0.2584 |     0.258  | H            |
