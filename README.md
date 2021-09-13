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

| Date       | HomeTeam         | AwayTeam         | pr_h_won |  pr_draw | pr_a_won | prediction | result |
|:----------:|------------------|------------------|---------:|---------:|---------:|:----------:|:------:|
| 2021-09-11 | Crystal   Palace | Tottenham        | 0.329318 | 0.326657 | 0.344026 | A          |      H |
| 2021-09-11 | Man. Utd         | Newcastle        | 0.377006 | 0.313049 | 0.309945 | H          |      H |
| 2021-09-11 | Brentford        | Brighton         | 0.334466 | 0.328736 | 0.336798 | D          |      A |
| 2021-09-11 | Watford          | Wolverhampton    | 0.333558 | 0.328423 | 0.338019 | D          |      A |
| 2021-09-11 | Arsenal          | Norwich          | 0.361551 |  0.32278 | 0.315669 | H          |      H |
| 2021-09-11 | Southampton      | West Ham         | 0.332461 | 0.324929 |  0.34261 | A          |      D |
| 2021-09-11 | Leicester        | Man. City        | 0.316791 | 0.322214 | 0.360995 | A          |      A |
| 2021-09-11 | Chelsea          | Aston Villa      | 0.377019 | 0.313615 | 0.309366 | H          |      H |
| 2021-09-12 | Leeds            | Liverpool        | 0.322159 | 0.327243 | 0.350598 | A          |      A |
| 2021-09-13 | Everton        | Burnley        |   0.363973 |  0.324074 |   0.311952 | H            |
| 2021-09-17 | Newcastle      | Leeds          |   0.335699 |  0.326577 |   0.337723 | A            |
| 2021-09-18 | Wolverhampton  | Brentford      |   0.349846 |  0.328648 |   0.321506 | H            |
| 2021-09-18 | Burnley        | Arsenal        |   0.331997 |  0.325836 |   0.342167 | A            |
| 2021-09-18 | Liverpool      | Crystal Palace |   0.375659 |  0.313657 |   0.310685 | H            |
| 2021-09-18 | Man. City      | Southampton    |   0.381051 |  0.310775 |   0.308174 | H            |
| 2021-09-18 | Norwich        | Watford        |   0.344787 |  0.327089 |   0.328124 | A            |
| 2021-09-18 | Aston Villa    | Everton        |   0.332298 |  0.330005 |   0.337697 | D            |
| 2021-09-19 | West Ham       | Man. Utd       |   0.3324   |  0.32487  |   0.342731 | A            |
| 2021-09-19 | Brighton       | Leicester      |   0.33882  |  0.328372 |   0.332808 | D            |
| 2021-09-19 | Tottenham      | Chelsea        |   0.331063 |  0.326115 |   0.342822 | A            |
| 2021-09-25 | Chelsea        | Man. City      |   0.337035 |  0.326111 |   0.336854 | A            |
| 2021-09-25 | Leeds          | West Ham       |   0.337256 |  0.325594 |   0.33715  | A            |
| 2021-09-25 | Man. Utd       | Aston Villa    |   0.379125 |  0.311984 |   0.30889  | H            |
| 2021-09-25 | Watford        | Newcastle      |   0.340254 |  0.325875 |   0.333871 | A            |
| 2021-09-25 | Leicester      | Burnley        |   0.365836 |  0.321578 |   0.312586 | H            |
| 2021-09-25 | Everton        | Norwich        |   0.370054 |  0.321849 |   0.308097 | H            |
| 2021-09-25 | Brentford      | Liverpool      |   0.314547 |  0.311838 |   0.373616 | A            |
| 2021-09-26 | Southampton    | Wolverhampton  |   0.335378 |  0.328339 |   0.336283 | D            |
| 2021-09-26 | Arsenal        | Tottenham      |   0.336386 |  0.32851  |   0.335103 | D            |
| 2021-09-27 | Crystal Palace | Brighton       |   0.331716 |  0.327426 |   0.340858 | A            |
