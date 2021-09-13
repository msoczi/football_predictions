# LOG
print('Read modules...')

import yaml
import os
import re
import pandas as pd
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import xgboost as xgb
from sklearn.tree import DecisionTreeClassifier
import pickle


########################################################################
################ Get settings from a configuration file ################
with open("config.yaml", 'r') as configuration:
    config = yaml.safe_load(configuration)


def predict_results(league):
    """
    Function returns table with matches info, odds, probability and prediction.
    
    Args:
        league (str): name of league for which predictions should be returned
    """


    ########################################################################
    ### Downloade data - results of matches from a given league ####
    if league == 'PremierLeague':
        req = requests.get('https://www.football-data.co.uk/mmz4281/'+config['season']+'/E0.csv')
    if league == 'Bundesliga':
        req = requests.get('https://www.football-data.co.uk/mmz4281/'+config['season']+'/D1.csv')
    if league == 'SerieA':
        req = requests.get('https://www.football-data.co.uk/mmz4281/'+config['season']+'/I1.csv')
    if league == 'LaLiga':
        req = requests.get('https://www.football-data.co.uk/mmz4281/'+config['season']+'/SP1.csv')
    url_content = req.content
    csv_file_results = open('E0.csv', 'wb')    # save results as E0.csv file
    csv_file_results.write(url_content)
    csv_file_results.close()


    ########################################################################
    # Tool for loading the CURRENT EO TABLE and creating model variables for prediction
    def calc_features(n, home_team, away_team):
        def read_data(n):
            # n=0 - get all rows
            # n=1 - remove 1 row
            # n=k - remove k row
            results = pd.read_csv('E0.csv', parse_dates=['Date'], dayfirst=True)
            results = results.drop(results.tail(n+1).index)
            return results

        results = read_data(0)
        results = results[['Date','HomeTeam','AwayTeam','FTHG','FTAG','FTR','HS','AS','HST','AST','HC','AC','HY','AY','HR','AR']]
        table = pd.DataFrame(set(results.HomeTeam), columns = ['Team'])
        results2 = results.copy()
        results2 = results2.drop(['HomeTeam'], axis=1)
        results2['HomeTeam'] = results2.AwayTeam
        results2 = results2.drop(['AwayTeam'], axis=1)
        results2['HoA'] = 'A'

        results['HoA'] = 'H'
        results = results.drop(['AwayTeam'], axis=1)
        results

        results = pd.concat([results, results2], axis=0,ignore_index=True)
        results.rename(columns={'HomeTeam':'Team'}, inplace=True)
        #results['Date'] = pd.to_datetime(results['Date'], format='%d/%m/%y')
        results = results.sort_values(by=['Date'], ascending=False)

        def punkty_zdobyte(results):
            if results.FTR == 'D':
                return 1
            if results.FTR == results.HoA:
                return 3
            if results.FTR != results.HoA:
                return 0

        def gole_zdobyte(results):
            if results.HoA == 'A':
                return results.FTAG
            if results.HoA == 'H':
                return results.FTHG

        def gole_stracone(results):
            if results.HoA == 'A':
                return results.FTHG
            if results.HoA == 'H':
                return results.FTAG

        def strzaly_oddane(results):
            if results.HoA == 'A':
                return results.AS
            if results.HoA == 'H':
                return results.HS

        def strzaly_otrzymane(results):
            if results.HoA == 'A':
                return results.HS
            if results.HoA == 'H':
                return results.AS

        def strz_cel_oddane(results):
            if results.HoA == 'A':
                return results.AST
            if results.HoA == 'H':
                return results.HST

        def strz_cel_otrzymane(results):
            if results.HoA == 'A':
                return results.HST
            if results.HoA == 'H':
                return results.AST

        def kornery_wykonane(results):
            if results.HoA == 'A':
                return results.AC
            if results.HoA == 'H':
                return results.HC

        def kornery_bronione(results):
            if results.HoA == 'A':
                return results.HC
            if results.HoA == 'H':
                return results.AC
        def otrzymane_zolte_kartki(results):
            if results.HoA == 'A':
                return results.AY
            if results.HoA == 'H':
                return results.HY

        def otrzymane_czerwone_kartki(results):
            if results.HoA == 'A':
                return results.AR
            if results.HoA == 'H':
                return results.HR


        results['pts'] = results.apply(lambda x: punkty_zdobyte(x), axis=1)
        results['goal_zdob'] = results.apply(lambda x: gole_zdobyte(x), axis=1)
        results['goal_strc'] = results.apply(lambda x: gole_stracone(x), axis=1)
        results['sh_odd'] = results.apply(lambda x: strzaly_oddane(x), axis=1)
        results['sh_otrz'] = results.apply(lambda x: strzaly_otrzymane(x), axis=1)
        results['sot_odd'] = results.apply(lambda x: strz_cel_oddane(x), axis=1)
        results['sot_otrz'] = results.apply(lambda x: strz_cel_otrzymane(x), axis=1)
        results['cor_wyk'] = results.apply(lambda x: kornery_wykonane(x), axis=1)
        results['cor_bro'] = results.apply(lambda x: kornery_bronione(x), axis=1)
        results['yel_card'] = results.apply(lambda x: otrzymane_zolte_kartki(x), axis=1)
        results['red_card'] = results.apply(lambda x: otrzymane_czerwone_kartki(x), axis=1)

        # Preparing data:
        # - group by HomeTeam
        # - we are reversing the datasets to take into consideration the latest matches

        def split(data, f):
            grouped = data.groupby(f)
            return [g for _, g in grouped], list(grouped.groups.keys())

        results_split, results_split_names = split(results, 'Team')
        # We take the form of the team - different versions are possible here

        # List of points scored in the last n matches
        def team_form_pts_mean(team, n):
            return team.pts[:n].mean()

        # Average goals scored in the last n matches
        def team_form_goal_mean(team, n):
            return team.goal_zdob[:n].mean()

        # Average goals conceded in the last n matches
        def team_form_goal_strac_mean(team, n):
            return team.goal_strc[:n].mean()

        # Average shots in the last n matches
        def team_form_shot_odd_mean(team, n):
            return team.sh_odd[:n].mean()

        # Average shots 'defended' in the last n matches
        def team_form_shot_otrz_mean(team, n):
            return team.sh_otrz[:n].mean()

        # Average shots on target in the last n matches
        def team_form_shot_trg_odd_mean(team, n):
            return team.sot_odd[:n].mean()

        # Average shots on target defended in the last n matches
        def team_form_shot_trg_otrz_mean(team, n):
            return team.sot_otrz[:n].mean()

        # Average of corners in the last n matches
        def team_form_cor_wyk_mean(team, n):
            return team.cor_wyk[:n].mean()

        # Average of corners defended in the last n matches
        def team_form_kor_bro_mean(team, n):
            return team.cor_bro[:n].mean()

        # Average number of yellow cards in the last n games
        def team_form_yel_card_mean(team, n):
            return team.yel_card[:n].mean()

        # Average number of red cards in the last n games
        def team_form_red_card_mean(team, n):
            return team.red_card[:n].mean()

        # Create variables
        form_var = pd.concat([pd.DataFrame(results_split_names),
                              # Variables based on the number of points scored in the last n matches
                               pd.DataFrame(list(map(lambda x: team_form_pts_mean(x, 3), results_split))),
                               pd.DataFrame(list(map(lambda x: team_form_pts_mean(x, 5), results_split))),
                               pd.DataFrame(list(map(lambda x: team_form_pts_mean(x, 7), results_split))),
                              # Variable based on the number of goals scored in the last n matches
                              pd.DataFrame(list(map(lambda x: team_form_goal_mean(x, 3), results_split))),
                              pd.DataFrame(list(map(lambda x: team_form_goal_mean(x, 5), results_split))),
                              pd.DataFrame(list(map(lambda x: team_form_goal_mean(x, 7), results_split))),
                              # Variables based on the number of goals conceded in the last n matches
                              pd.DataFrame(list(map(lambda x: team_form_goal_strac_mean(x, 3), results_split))),
                              pd.DataFrame(list(map(lambda x: team_form_goal_strac_mean(x, 5), results_split))),
                              pd.DataFrame(list(map(lambda x: team_form_goal_strac_mean(x, 7), results_split))),
                              # Variable based on the number of shots fired in the last n matches
                              pd.DataFrame(list(map(lambda x: team_form_shot_odd_mean(x, 3), results_split))),
                              pd.DataFrame(list(map(lambda x: team_form_shot_odd_mean(x, 5), results_split))),
                              pd.DataFrame(list(map(lambda x: team_form_shot_odd_mean(x, 7), results_split))),
                              # Variables based on the number of shots received in the last n matches
                              pd.DataFrame(list(map(lambda x: team_form_shot_otrz_mean(x, 3), results_split))),
                              pd.DataFrame(list(map(lambda x: team_form_shot_otrz_mean(x, 5), results_split))),
                              pd.DataFrame(list(map(lambda x: team_form_shot_otrz_mean(x, 7), results_split))),

                              # Variables based on the number of shots fired in the last n matches
                              pd.DataFrame(list(map(lambda x: team_form_shot_trg_odd_mean(x, 3), results_split))),
                              pd.DataFrame(list(map(lambda x: team_form_shot_trg_odd_mean(x, 5), results_split))),
                              pd.DataFrame(list(map(lambda x: team_form_shot_trg_odd_mean(x, 7), results_split))),
                              # Variables based on the number of shots received in the last n matches
                              pd.DataFrame(list(map(lambda x: team_form_shot_trg_otrz_mean(x, 3), results_split))),
                              pd.DataFrame(list(map(lambda x: team_form_shot_trg_otrz_mean(x, 5), results_split))),
                              pd.DataFrame(list(map(lambda x: team_form_shot_trg_otrz_mean(x, 7), results_split))),

                              # Variables based on the number of corners in the last n matches
                              pd.DataFrame(list(map(lambda x: team_form_cor_wyk_mean(x, 3), results_split))),
                              pd.DataFrame(list(map(lambda x: team_form_cor_wyk_mean(x, 5), results_split))),
                              pd.DataFrame(list(map(lambda x: team_form_cor_wyk_mean(x, 7), results_split))),
                              # Variables based on the number of corners defended in the last n matches
                              pd.DataFrame(list(map(lambda x: team_form_kor_bro_mean(x, 3), results_split))),
                              pd.DataFrame(list(map(lambda x: team_form_kor_bro_mean(x, 5), results_split))),
                              pd.DataFrame(list(map(lambda x: team_form_kor_bro_mean(x, 7), results_split))),
                              # Variables based on the number of yellow cards in the last n matches
                              pd.DataFrame(list(map(lambda x: team_form_yel_card_mean(x, 3), results_split))),
                              pd.DataFrame(list(map(lambda x: team_form_yel_card_mean(x, 5), results_split))),
                              pd.DataFrame(list(map(lambda x: team_form_yel_card_mean(x, 7), results_split))),
                              # Variable based on the number of red cards in the last n matches
                              pd.DataFrame(list(map(lambda x: team_form_red_card_mean(x, 3), results_split))),
                              pd.DataFrame(list(map(lambda x: team_form_red_card_mean(x, 5), results_split))),
                              pd.DataFrame(list(map(lambda x: team_form_red_card_mean(x, 7), results_split))),
                              ],axis=1,ignore_index=True)

        # Change names of variables
        form_var.columns = ['Team',
                            'pts_3','pts_5','pts_7',
                            'gz_3','gz_5','gz_7',
                            'gs_3','gs_5','gs_7',
                            'sh_od_3','sh_od_5','sh_od_7',
                            'sh_ot_3','sh_ot_5','sh_ot_7',
                            'sot_od_3','sot_od_5','sot_od_7',
                            'sot_ot_3','sot_ot_5','sot_ot_7',
                            'cw_3','cw_5','cw_7',
                            'cb_3','cb_5','cb_7',
                            'yc_3','yc_5','yc_7',
                            'rc_3','rc_5','rc_7',
                           ]

        form_var = form_var.set_index('Team')

        ###################################################################
        # Create a league table and other variables (not based on time)
        ###################################################################

        results = read_data(n)
        results = results[['Date','HomeTeam','AwayTeam','FTHG','FTAG','FTR','HS','AS','HST','AST','HC','AC']]

        def home_points(results):
            if results.FTR == 'H':
                return 3
            if results.FTR == 'A':
                return 0
            if results.FTR == 'D':
                return 1

        def away_points(results):
            if results.FTR == 'H':
                return 0
            if results.FTR == 'A':
                return 3
            if results.FTR == 'D':
                return 1

        results['H_pts'] = results.apply(lambda x: home_points(x), axis=1)
        results['A_pts'] = results.apply(lambda x: away_points(x), axis=1)

        home_table = results.groupby('HomeTeam').sum()[['FTHG','FTAG','HS','AS','HST','AST','HC','AC','H_pts']]
        away_table = results.groupby('AwayTeam').sum()[['FTHG','FTAG','HS','AS','HST','AST','HC','AC','A_pts']]
        home_table.columns = ['H_goal_zdob','H_goal_strc','H_strzaly_oddane','H_strzaly_dopuszczone','H_strz_cel_oddane','H_strz_cel_dopuszczone','H_kornery_wyk','H_kornery_bro','H_pts']
        away_table.columns = ['A_goal_strc','A_goal_zdob','A_strzaly_dopuszczone','A_strzaly_oddane','A_strz_cel_oddane','A_strz_cel_dopuszczone','A_kornery_wyk','A_kornery_bro','A_pts']

        res_table = pd.concat([home_table, away_table], axis=1)

        res_table['goal_zdob'] = res_table.H_goal_zdob + res_table.A_goal_zdob
        res_table['goal_strc'] = res_table.H_goal_strc + res_table.A_goal_strc
        res_table['goal_bilans'] = res_table.goal_zdob - res_table.goal_strc
        res_table['pts'] = res_table.H_pts + res_table.A_pts

        res_table['strzaly_oddane'] = res_table.H_strzaly_oddane + res_table.A_strzaly_oddane
        res_table['strzaly_dopuszczone'] = res_table.H_strzaly_dopuszczone + res_table.A_strzaly_dopuszczone
        res_table['strz_cel_oddane'] = res_table.H_strz_cel_oddane + res_table.A_strz_cel_oddane
        res_table['strz_cel_dopuszczone'] = res_table.H_strz_cel_dopuszczone + res_table.A_strz_cel_dopuszczone

        res_table['cor_wyk'] = res_table.H_kornery_wyk + res_table.A_kornery_wyk
        res_table['cor_bro'] = res_table.H_kornery_bro + res_table.A_kornery_bro

        # Sort by points - we create an imitation of the table
        res_table.sort_values(by=['pts','goal_bilans','goal_zdob'], inplace=True, ascending=(False,False,False))
        # NOTE: In the case of an equal number of points, the position in the table depends on the rules by specific league.
        # We will always assume the order: pts'> 'goal_bilans'>' goal_zdob '


        # Number of matches played at home and away
        res_table['H_nmatch'] = results.groupby('HomeTeam').size()
        res_table['A_nmatch'] = results.groupby('AwayTeam').size()
        res_table['n_match'] = res_table['H_nmatch'] + res_table['A_nmatch']

        # Create characteristics
        res_table['pts_per_math'] = res_table.pts/res_table.n_match
        res_table['gz'] = res_table.goal_zdob/res_table.n_match
        res_table['gs'] = res_table.goal_strc/res_table.n_match
        res_table['sh_od'] = res_table.strzaly_oddane/res_table.n_match
        res_table['sh_ot'] = res_table.strzaly_dopuszczone/res_table.n_match
        res_table['cw'] = res_table.cor_wyk/res_table.n_match
        res_table['cb'] = res_table.cor_bro/res_table.n_match
        res_table['pozycja'] = range(1,len(res_table)+1)
        res_table

        ###########################################################################
        # The (almost) output table - data with created variables
        ###########################################################################

        output = pd.concat([form_var,
                            res_table[['pts_per_math','gz','gs','sh_od','sh_ot','cw','cb','pozycja']]
                           ], axis=1)

        h_var = output.loc[[home_team] , : ]
        h_var.columns = ['h_'+i for i in h_var.columns]
        h_var.index = [0]

        a_var = output.loc[[away_team] , : ]
        a_var.columns = ['a_'+i for i in a_var.columns]
        a_var.index = [0]

        return pd.concat([h_var, a_var], axis=1)


    ####################################################################################
    # Scraping future matches and their odds from the STS website
    page = requests.get(config['scraping'][league])
    soup = BeautifulSoup(page.content, 'html.parser')

    table = soup.findAll("table", { "class" : "subTable"})

    def take_courses(x):
        return re.sub('\n+', '\n', x.text).lstrip().rstrip().split('\n')

    def take_date(x):
        return str(x.find("td", {"class" : "bet bigTip"})).split("oppty_end_date",1)[1][3:13]

    courses = pd.DataFrame(map(take_courses, table))
    dates = pd.DataFrame(map(take_date, table))

    courses = pd.concat([courses, dates], axis=1, ignore_index=True)
    del dates
    courses.columns = ['HomeTeam','h_course','x','d_course','AwayTeam','a_course','Date']

    # zapisujemy tabelke z kursami
    courses.to_csv('courses.csv')


    ####################################################################################
    # Creating a vars_to_predict file and create variables for a given team
    teams_names_dict = config['teams_names_dict'][league]

    for i in range(len(courses)):
        HOME_TEAM = teams_names_dict[courses.iloc[i,0]]
        AWAY_TEAM = teams_names_dict[courses.iloc[i,4]]

        h_kurs = courses.iloc[i,1]
        d_kurs = courses.iloc[i,3]
        a_kurs = courses.iloc[i,5]

        kursy_concat = pd.DataFrame([[h_kurs,d_kurs,a_kurs]], columns = ['h_course','d_course','a_course'])

        if i == 0:
            pd.concat([kursy_concat,
                  calc_features(0, home_team = HOME_TEAM, away_team = AWAY_TEAM)
                  ], axis=1).to_csv('vars_to_predict.csv', mode='a', header=True)
        else:
            pd.concat([kursy_concat,
                  calc_features(0, home_team = HOME_TEAM, away_team = AWAY_TEAM)
                  ], axis=1).to_csv('vars_to_predict.csv', mode='a', header=False)



    ####################################################################################
    # Prediction and summary result 
    data_to_predict = pd.read_csv('vars_to_predict.csv', sep=',')
    data_to_predict = data_to_predict.drop(['Unnamed: 0'], axis=1)

    courses = pd.read_csv('courses.csv', sep=',')
    courses = courses.drop(['Unnamed: 0','x'], axis=1)
    courses = courses[['Date','h_course','HomeTeam','d_course','AwayTeam','a_course']]

    # Uploading models and components
    xgb_model = pickle.load(open('model\\xgb_model.pkl', "rb"))
    tree_model = pickle.load(open('model\\tree_model.pkl', "rb"))
    dicts2translate = pickle.load(open('model\\dicts2translate.pkl', "rb"))

    # Prediction
    data_to_predict = xgb.DMatrix(data_to_predict)
    preds = pd.DataFrame(xgb_model.predict(data_to_predict))
    
    courses['pr_h_won'] = preds[0]
    courses['pr_draw']  = preds[1]
    courses['pr_a_won'] = preds[2]
    
    # Remove courses form returned table - remove this part if you would like to keep courses
    courses = courses.drop(['h_course','d_course','a_course'], axis=1)
    

    #######
    # Add a column with information about who will win the match according to the decision tree
    tree_preds = tree_model.predict(preds)
    preds_after_translation = [dicts2translate['idx2str'][elem] for elem in tree_preds]
    courses['prediction'] = preds_after_translation

    # Remove unnecessary temporary files
    os.remove('vars_to_predict.csv')
    os.remove('E0.csv')
    os.remove('courses.csv')

    return courses
    

# LOG
print('Predictions for',config['league'], 'in progress...')

# Run function for premier league
courses = predict_results(league = config['league'])

# Save output in .md file
with open('output.md', 'w') as file:
    file.write(courses.to_markdown(index = False))

# LOG
print('Process complited!\n Output in:', 'output.md')

