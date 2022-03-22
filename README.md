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
| 2022-04-02 |       1.13 | Liverpool      |       8.85 | Watford        |      18.5  |     0.758  |    0.1541 |     0.088  | H            |
| 2022-04-02 |       2.36 | Leeds          |       3.45 | Southampton    |       2.8  |     0.2884 |    0.2221 |     0.4895 | A            |
| 2022-04-02 |       2.8  | Wolverhampton  |       3.05 | Aston Villa    |       2.65 |     0.4825 |    0.2429 |     0.2746 | H            |
| 2022-04-02 |       1.35 | Chelsea        |       4.85 | Brentford      |       8.95 |     0.7486 |    0.1558 |     0.0955 | H            |
| 2022-04-02 |      12.75 | Burnley        |       6.6  | Man. City      |       1.21 |     0.1384 |    0.1773 |     0.6843 | A            |
| 2022-04-02 |       1.63 | Brighton       |       3.7  | Norwich        |       5.5  |     0.5352 |    0.2515 |     0.2133 | H            |
| 2022-04-02 |       1.56 | Man. Utd       |       4.25 | Leicester      |       5.3  |     0.6394 |    0.1957 |     0.1649 | H            |
| 2022-04-03 |       1.82 | West Ham       |       3.6  | Everton        |       4.2  |     0.6495 |    0.1856 |     0.1649 | H            |
| 2022-04-03 |       1.51 | Tottenham      |       4.25 | Newcastle      |       5.95 |     0.5023 |    0.226  |     0.2717 | H            |
| 2022-04-04 |       3.95 | Crystal Palace |       3.3  | Arsenal        |       1.95 |     0.2586 |    0.2529 |     0.4884 | A            |
| 2022-04-06 |       2.6  | Burnley        |       3.15 | Everton        |       2.7  |     0.4414 |    0.2587 |     0.2998 | H            |
| 2022-04-08 |       2.48 | Newcastle      |       3.05 | Wolverhampton  |       2.95 |     0.5233 |    0.2426 |     0.2341 | H            |
| 2022-04-09 |       4.25 | Everton        |       3.7  | Man. Utd       |       1.78 |     0.205  |    0.2002 |     0.5948 | A            |
| 2022-04-09 |       4.85 | Southampton    |       3.8  | Chelsea        |       1.68 |     0.3077 |    0.2343 |     0.458  | A            |
| 2022-04-09 |       2.8  | Watford        |       3.2  | Leeds          |       2.5  |     0.4312 |    0.2264 |     0.3424 | A            |
| 2022-04-09 |       1.61 | Arsenal        |       3.85 | Brighton       |       5.35 |     0.6917 |    0.1919 |     0.1164 | H            |
| 2022-04-09 |       3    | Aston Villa    |       3.25 | Tottenham      |       2.36 |     0.3319 |    0.2623 |     0.4058 | D            |
| 2022-04-10 |       2.75 | Norwich        |       3.15 | Burnley        |       2.6  |     0.3873 |    0.2873 |     0.3254 | D            |
| 2022-04-10 |       3.2  | Brentford      |       3.3  | West Ham       |       2.22 |     0.3176 |    0.2654 |     0.417  | D            |
| 2022-04-10 |       2.16 | Leicester      |       3.35 | Crystal Palace |       3.3  |     0.4024 |    0.2847 |     0.3129 | D            |
| 2022-04-10 |       2.11 | Man. City      |       3.5  | Liverpool      |       3.25 |     0.46   |    0.2002 |     0.3398 | A            |
