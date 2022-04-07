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
The XGBoost model was built on a hand-prepared historical sample containing 7210 rows and 354 columns. As the objective function, `multi:softprob` was used so that the model's output was the probability of assigning observations to each of the 3 classes of match result - H (Home), A (Away), D (Draw).
<br>
These probabilities were then used to build a simple decision tree (`max_depth = 3`) that would allow to categorize individual observations in a rule-based manner, i.e. to predict the final result with simple rules. This procedure allowed for the generalization of the results in such a way that the draw was not too rare. Below is the sheme of decision tree.
<br>
![tree](model/img_tree.PNG)

Forecasts **do not use bookmaker odds**. I provide them for information only.
<br>
<br>
So far, no API has been developed that allows for the ongoing tracking of progzones and their results.
<br>
However, it is possible to clone the repository and use it with python.
<br>
How to use?
1. Clone repository.
```sh
git clone https://github.com/msoczi/football_predictions
```
2. Create and activate virtual environment for python.
LINUX:
```sh
python3 -m venv football_preds
source football_preds/bin/activate

```
WINDOWS:
```sh
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
<br>
 
### Upcoming Premier League matches

|    Date    |  H - odds  | HomeTeam       |  D - odds  | AwayTeam       |  A - odds  | prob H win | prob draw | prob A win |  Prediction  |
|:-----------|-----------:|:---------------|-----------:|:---------------|-----------:|-----------:|----------:|-----------:|:-------------|
| 2022-04-08 |       2.35 | Newcastle   |       3.2  | Wolverhampton  |       3.2  |     0.4216 |    0.2802 |     0.2981 | D            |
| 2022-04-09 |       4.3  | Everton     |       3.7  | Man. Utd       |       1.77 |     0.2113 |    0.2201 |     0.5686 | A            |
| 2022-04-09 |       3.9  | Southampton |       3.5  | Chelsea        |       1.9  |     0.2208 |    0.2151 |     0.5641 | A            |
| 2022-04-09 |       2.6  | Watford     |       3.4  | Leeds          |       2.55 |     0.4555 |    0.2326 |     0.3119 | A            |
| 2022-04-09 |       1.62 | Arsenal     |       4    | Brighton       |       5.45 |     0.6725 |    0.1896 |     0.138  | H            |
| 2022-04-09 |       3.05 | Aston Villa |       3.35 | Tottenham      |       2.26 |     0.2772 |    0.2113 |     0.5115 | A            |
| 2022-04-10 |       2.85 | Norwich     |       3.05 | Burnley        |       2.55 |     0.3835 |    0.2861 |     0.3304 | D            |
| 2022-04-10 |       2.75 | Brentford   |       3.2  | West Ham       |       2.55 |     0.3857 |    0.2404 |     0.3739 | A            |
| 2022-04-10 |       2.33 | Leicester   |       3.3  | Crystal Palace |       2.95 |     0.3559 |    0.303  |     0.3411 | D            |
| 2022-04-10 |       2.04 | Man. City   |       3.55 | Liverpool      |       3.4  |     0.4618 |    0.1972 |     0.341  | A            |
| 2022-04-16 |       1.62 | Tottenham   |       3.8  | Brighton       |       5.35 |     0.6373 |    0.1616 |     0.2011 | H            |
| 2022-04-16 |       2.7  | Watford     |       3.1  | Brentford      |       2.7  |     0.3919 |    0.2532 |     0.3549 | A            |
| 2022-04-16 |       3.5  | Southampton |       3.3  | Arsenal        |       2.07 |     0.2937 |    0.2457 |     0.4606 | A            |
| 2022-04-16 |       1.23 | Man. Utd    |       6.4  | Norwich        |      12.25 |     0.6714 |    0.1997 |     0.1289 | H            |
| 2022-04-17 |       1.56 | West Ham    |       3.95 | Burnley        |       5.85 |     0.6091 |    0.2211 |     0.1698 | H            |
| 2022-04-17 |       2.5  | Newcastle   |       3.15 | Leicester      |       2.85 |     0.3829 |    0.2416 |     0.3755 | A            |
