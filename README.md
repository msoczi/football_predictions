## Football matches result predictions
______________
For page with results refer to: **https://msoczi.github.io/football_predictions/web/index.html** 
______________
The aim of the project was to create a tool for predicting the results of league matches from the leading European leagues based on data prepared by myself.

The project was implemented _from scratch_, i.e. it included:
- collection of raw data on the basis of which it will be possible to create characteristics and then modeling
- creating variables based on i.a. time aggregates (last n matches), position in the table, team form, etc.
- calculate historical data for modeling
- building the target solution: XGBoost model with 3 classes. Then, based on the estimated probability, a decision tree was created, which in a simple, rule-based way predicts which team will win the match (or a possible draw)
- creating a script that downloads data about upcoming matches, creating model variables for given teams and prediction of the match result.

Raw data with match results are downloaded from https://www.football-data.co.uk. <br>
The advantage of the approach is the ability to predict results from any league. But o far, it is possible to predict the results of the first league of the following countries:
- ![England](https://raw.githubusercontent.com/stevenrskelton/flag-icon/master/png/16/country-4x3/gb.png "England") England
- ![Italy](https://raw.githubusercontent.com/stevenrskelton/flag-icon/master/png/16/country-4x3/it.png "Italy") Italy
- ![Germany](https://raw.githubusercontent.com/stevenrskelton/flag-icon/master/png/16/country-4x3/de.png "Germany") Germany
- ![Spain](https://raw.githubusercontent.com/stevenrskelton/flag-icon/master/png/16/country-4x3/es.png "Spain") Spain
- ![France](https://raw.githubusercontent.com/stevenrskelton/flag-icon/master/png/16/country-4x3/fr.png "France") France


Based on the raw data, I created the appropriate characteristics by myself. The full list of variables is available in the file: <a href="model/variables.md">variables</a>
<br>
<br>
The XGBoost model was built on a hand-prepared historical sample containing 7210 rows and 354 columns. As the objective function, `multi:softprob` was used so that the model's output was the probability of assigning observations to each of the 3 classes of match result - **H (Home), A (Away), D (Draw)**.
<br>
These probabilities were then used to build a simple decision tree (`max_depth = 3`) that would allow to categorize individual observations in a rule-based manner, i.e. to predict the final result with simple rules. This procedure allowed for the generalization of the results in such a way that the draw was not too rare. Below is the sheme of decision tree.
<br>
![tree](model/img_tree.PNG)

Forecasts **do not use bookmaker odds**.
<br>
<br>
You can view the results on the site:

### **https://msoczi.github.io/football_predictions/web/index.html** 


You can also clone the repository and use it with python.
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
python scripts/main_script.py <LEAGUE_NAME>
```
Then results will be saved to `\output_tables` for league passed in the argument.
