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
git clone https://github.com/msoczi/YOUR-REPOSITORY
```
You can use the package in two ways:
1. Interactive - via Jupyter Notebook - as the main function argument pass the name of the league for which you want to get forecasts. 
2. Run the <a href="main_script.py">main_script.py</a> from console e.g. 
```sh
python main_script.py
```
Then results will be saved to output.md file for league passed in the configuration file <a href="config.yaml">config.yaml</a>.
