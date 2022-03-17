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
| 2022-03-17 |       2.5  | Everton        |       3.25 | Newcastle   |       2.9  |     0.1684 |    0.3317 |     0.4998 | D            |
| 2022-03-18 |       2.15 | Wolverhampton  |       3.45 | Leeds       |       3.4  |     0.5856 |    0.302  |     0.1124 | H            |
| 2022-03-19 |       2.95 | Aston Villa    |       3.35 | Arsenal     |       2.34 |     0.3606 |    0.2252 |     0.4143 | A            |
| 2022-03-20 |       2.12 | Leicester      |       3.35 | Brentford   |       3.35 |     0.5816 |    0.2665 |     0.1519 | H            |
| 2022-03-20 |       1.72 | Tottenham      |       3.85 | West Ham    |       4.45 |     0.5988 |    0.1799 |     0.2213 | H            |
| 2022-04-02 |       1.13 | Liverpool      |       8.85 | Watford     |      18.75 |     0.8422 |    0.1012 |     0.0566 | H            |
| 2022-04-02 |       2.43 | Leeds          |       3.35 | Southampton |       2.8  |     0.1797 |    0.2774 |     0.5429 | A            |
| 2022-04-02 |       2.6  | Wolverhampton  |       3.05 | Aston Villa |       2.85 |     0.4271 |    0.3267 |     0.2462 | D            |
| 2022-04-02 |       1.33 | Chelsea        |       5    | Brentford   |       9.5  |     0.8384 |    0.1067 |     0.0549 | H            |
| 2022-04-02 |      12.25 | Burnley        |       6.6  | Man. City   |       1.22 |     0.1326 |    0.1826 |     0.6848 | A            |
| 2022-04-02 |       1.57 | Brighton       |       3.85 | Norwich     |       5.9  |     0.4522 |    0.3689 |     0.1789 | D            |
| 2022-04-02 |       1.53 | Man. Utd       |       4.45 | Leicester   |       5.4  |     0.6759 |    0.203  |     0.1211 | H            |
| 2022-04-03 |       1.76 | West Ham       |       3.6  | Everton     |       4.5  |     0.6585 |    0.2535 |     0.0879 | H            |
| 2022-04-03 |       1.56 | Tottenham      |       4.1  | Newcastle   |       5.55 |     0.5486 |    0.2678 |     0.1836 | H            |
| 2022-04-04 |       4.05 | Crystal Palace |       3.35 | Arsenal     |       1.91 |     0.271  |    0.2488 |     0.4803 | A            |
