# LOG
print('Read modules...')

import yaml
import os
import re
import pandas as pd
import numpy as np
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
        """
        Function returns table with created variables.
        
        Args:
            n (int): ??? is it still necessary 
            
            home_team (str): name of home team to create variables
            
            away_team (str): name of away team to create variables
        """
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
        
        def create_var_based_on_column(results, return_if_A, return_if_H):
            if results.HoA == 'A':
                return results[return_if_A]
            if results.HoA == 'H':
                return results[return_if_H]
        
        
        results['pts'] = results.apply(lambda x: punkty_zdobyte(x), axis=1)
        results['goal_zdob'] = results.apply(lambda x: create_var_based_on_column(x,'FTAG','FTHG'), axis=1) # gole zdobyte
        results['goal_strc'] = results.apply(lambda x: create_var_based_on_column(x,'FTHG','FTAG'), axis=1) # gole stracone
        results['sh_odd'] = results.apply(lambda x: create_var_based_on_column(x,'AS','HS'), axis=1) # strzaly_oddane
        results['sh_otrz'] = results.apply(lambda x: create_var_based_on_column(x,'HS','AS'), axis=1) # strzaly_otrzymane
        results['sot_odd'] = results.apply(lambda x: create_var_based_on_column(x,'AST','HST'), axis=1) # strz_cel_oddane
        results['sot_otrz'] = results.apply(lambda x: create_var_based_on_column(x,'HST','AST'), axis=1) # strz_cel_otrzymane
        results['cor_wyk'] = results.apply(lambda x: create_var_based_on_column(x,'AC','HC'), axis=1) # kornery_wykonane
        results['cor_bro'] = results.apply(lambda x: create_var_based_on_column(x,'HC','AC'), axis=1) # kornery_bronione
        results['yel_card'] = results.apply(lambda x: create_var_based_on_column(x,'AY','HY'), axis=1) # otrzymane_zolte_kartki
        results['red_card'] = results.apply(lambda x: create_var_based_on_column(x,'HY','AY'), axis=1) # otrzymane_czerwone_kartki

        # Preparing data:
        # - group by HomeTeam
        # - we are reversing the datasets to take into consideration the latest matches

        def split(data, f):
            grouped = data.groupby(f)
            return [g for _, g in grouped], list(grouped.groups.keys())

        results_split, results_split_names = split(results, 'Team')
        # We take the form of the team - different versions are possible here


        # Function create aggregate variable
        def create_aggregate_based_on_variables(team, n, var, stat):
            return stat(team[var][:n])
       
       
       
        # Create variables (aggregates)
        form_var = pd.concat([pd.DataFrame(results_split_names),
                          # Zmiene oparte na liczbie zdobytych punktów w ostatnich n meczach
                          pd.DataFrame(list(map(lambda x: create_aggregate_based_on_variables(x, 3, 'pts', np.mean), results_split))),
                          pd.DataFrame(list(map(lambda x: create_aggregate_based_on_variables(x, 5, 'pts', np.mean), results_split))),
                          pd.DataFrame(list(map(lambda x: create_aggregate_based_on_variables(x, 7, 'pts', np.mean), results_split))),
                          pd.DataFrame(list(map(lambda x: create_aggregate_based_on_variables(x, 3, 'pts', np.std), results_split))),
                          pd.DataFrame(list(map(lambda x: create_aggregate_based_on_variables(x, 5, 'pts', np.std), results_split))),
                          pd.DataFrame(list(map(lambda x: create_aggregate_based_on_variables(x, 7, 'pts', np.std), results_split))),
                          # Zmiene oparte na liczbie zdobytych bramek w ostatnich n meczach
                          pd.DataFrame(list(map(lambda x: create_aggregate_based_on_variables(x, 3, 'goal_zdob', np.mean), results_split))),
                          pd.DataFrame(list(map(lambda x: create_aggregate_based_on_variables(x, 5, 'goal_zdob', np.mean), results_split))),
                          pd.DataFrame(list(map(lambda x: create_aggregate_based_on_variables(x, 7, 'goal_zdob', np.mean), results_split))),
                          pd.DataFrame(list(map(lambda x: create_aggregate_based_on_variables(x, 3, 'goal_zdob', np.std), results_split))),
                          pd.DataFrame(list(map(lambda x: create_aggregate_based_on_variables(x, 5, 'goal_zdob', np.std), results_split))),
                          pd.DataFrame(list(map(lambda x: create_aggregate_based_on_variables(x, 7, 'goal_zdob', np.std), results_split))),
                          # Zmiene oparte na liczbie straconych bramek w ostatnich n meczach
                          pd.DataFrame(list(map(lambda x: create_aggregate_based_on_variables(x, 3, 'goal_strc', np.mean), results_split))),
                          pd.DataFrame(list(map(lambda x: create_aggregate_based_on_variables(x, 5, 'goal_strc', np.mean), results_split))),
                          pd.DataFrame(list(map(lambda x: create_aggregate_based_on_variables(x, 7, 'goal_strc', np.mean), results_split))),
                          pd.DataFrame(list(map(lambda x: create_aggregate_based_on_variables(x, 3, 'goal_strc', np.std), results_split))),
                          pd.DataFrame(list(map(lambda x: create_aggregate_based_on_variables(x, 5, 'goal_strc', np.std), results_split))),
                          pd.DataFrame(list(map(lambda x: create_aggregate_based_on_variables(x, 7, 'goal_strc', np.std), results_split))),
                          # Zmiene oparte na liczbie oddanych strzałów w ostatnich n meczach
                          pd.DataFrame(list(map(lambda x: create_aggregate_based_on_variables(x, 3, 'sh_odd', np.mean), results_split))),
                          pd.DataFrame(list(map(lambda x: create_aggregate_based_on_variables(x, 5, 'sh_odd', np.mean), results_split))),
                          pd.DataFrame(list(map(lambda x: create_aggregate_based_on_variables(x, 7, 'sh_odd', np.mean), results_split))),
                          pd.DataFrame(list(map(lambda x: create_aggregate_based_on_variables(x, 3, 'sh_odd', np.std), results_split))),
                          pd.DataFrame(list(map(lambda x: create_aggregate_based_on_variables(x, 5, 'sh_odd', np.std), results_split))),
                          pd.DataFrame(list(map(lambda x: create_aggregate_based_on_variables(x, 7, 'sh_odd', np.std), results_split))),
                          # Zmiene oparte na liczbie otrzymanych strzałów w ostatnich n meczach
                          pd.DataFrame(list(map(lambda x: create_aggregate_based_on_variables(x, 3, 'sh_otrz', np.mean), results_split))),
                          pd.DataFrame(list(map(lambda x: create_aggregate_based_on_variables(x, 5, 'sh_otrz', np.mean), results_split))),
                          pd.DataFrame(list(map(lambda x: create_aggregate_based_on_variables(x, 7, 'sh_otrz', np.mean), results_split))),
                          pd.DataFrame(list(map(lambda x: create_aggregate_based_on_variables(x, 3, 'sh_otrz', np.std), results_split))),
                          pd.DataFrame(list(map(lambda x: create_aggregate_based_on_variables(x, 5, 'sh_otrz', np.std), results_split))),
                          pd.DataFrame(list(map(lambda x: create_aggregate_based_on_variables(x, 7, 'sh_otrz', np.std), results_split))),
                          # Zmiene oparte na liczbie oddanych strzałów w ostatnich n meczach
                          pd.DataFrame(list(map(lambda x: create_aggregate_based_on_variables(x, 3, 'sot_odd', np.mean), results_split))),
                          pd.DataFrame(list(map(lambda x: create_aggregate_based_on_variables(x, 5, 'sot_odd', np.mean), results_split))),
                          pd.DataFrame(list(map(lambda x: create_aggregate_based_on_variables(x, 7, 'sot_odd', np.mean), results_split))),
                          pd.DataFrame(list(map(lambda x: create_aggregate_based_on_variables(x, 3, 'sot_odd', np.std), results_split))),
                          pd.DataFrame(list(map(lambda x: create_aggregate_based_on_variables(x, 5, 'sot_odd', np.std), results_split))),
                          pd.DataFrame(list(map(lambda x: create_aggregate_based_on_variables(x, 7, 'sot_odd', np.std), results_split))),
                          # Zmiene oparte na liczbie otrzymanych strzałów w ostatnich n meczach
                          pd.DataFrame(list(map(lambda x: create_aggregate_based_on_variables(x, 3, 'sot_otrz', np.mean), results_split))),
                          pd.DataFrame(list(map(lambda x: create_aggregate_based_on_variables(x, 5, 'sot_otrz', np.mean), results_split))),
                          pd.DataFrame(list(map(lambda x: create_aggregate_based_on_variables(x, 7, 'sot_otrz', np.mean), results_split))),
                          pd.DataFrame(list(map(lambda x: create_aggregate_based_on_variables(x, 3, 'sot_otrz', np.std), results_split))),
                          pd.DataFrame(list(map(lambda x: create_aggregate_based_on_variables(x, 5, 'sot_otrz', np.std), results_split))),
                          pd.DataFrame(list(map(lambda x: create_aggregate_based_on_variables(x, 7, 'sot_otrz', np.std), results_split))),
                          # Zmiene oparte na liczbie kornerów wykonanych w ostatnich n meczach
                          pd.DataFrame(list(map(lambda x: create_aggregate_based_on_variables(x, 3, 'cor_wyk', np.mean), results_split))),
                          pd.DataFrame(list(map(lambda x: create_aggregate_based_on_variables(x, 5, 'cor_wyk', np.mean), results_split))),
                          pd.DataFrame(list(map(lambda x: create_aggregate_based_on_variables(x, 7, 'cor_wyk', np.mean), results_split))),
                          pd.DataFrame(list(map(lambda x: create_aggregate_based_on_variables(x, 3, 'cor_wyk', np.std), results_split))),
                          pd.DataFrame(list(map(lambda x: create_aggregate_based_on_variables(x, 5, 'cor_wyk', np.std), results_split))),
                          pd.DataFrame(list(map(lambda x: create_aggregate_based_on_variables(x, 7, 'cor_wyk', np.std), results_split))),
                          # Zmiene oparte na liczbie korneró bronionych w ostatnich n meczach
                          pd.DataFrame(list(map(lambda x: create_aggregate_based_on_variables(x, 3, 'cor_bro', np.mean), results_split))),
                          pd.DataFrame(list(map(lambda x: create_aggregate_based_on_variables(x, 5, 'cor_bro', np.mean), results_split))),
                          pd.DataFrame(list(map(lambda x: create_aggregate_based_on_variables(x, 7, 'cor_bro', np.mean), results_split))),
                          pd.DataFrame(list(map(lambda x: create_aggregate_based_on_variables(x, 3, 'cor_bro', np.std), results_split))),
                          pd.DataFrame(list(map(lambda x: create_aggregate_based_on_variables(x, 5, 'cor_bro', np.std), results_split))),
                          pd.DataFrame(list(map(lambda x: create_aggregate_based_on_variables(x, 7, 'cor_bro', np.std), results_split))),
                          # Zmiene oparte na liczbie zółtych kartek w ostatnich n meczach
                          pd.DataFrame(list(map(lambda x: create_aggregate_based_on_variables(x, 3, 'yel_card', np.mean), results_split))),
                          pd.DataFrame(list(map(lambda x: create_aggregate_based_on_variables(x, 5, 'yel_card', np.mean), results_split))),
                          pd.DataFrame(list(map(lambda x: create_aggregate_based_on_variables(x, 7, 'yel_card', np.mean), results_split))),
                          pd.DataFrame(list(map(lambda x: create_aggregate_based_on_variables(x, 3, 'yel_card', np.std), results_split))),
                          pd.DataFrame(list(map(lambda x: create_aggregate_based_on_variables(x, 5, 'yel_card', np.std), results_split))),
                          pd.DataFrame(list(map(lambda x: create_aggregate_based_on_variables(x, 7, 'yel_card', np.std), results_split))),
                          # Zmiene oparte na liczbie czerwonych kartek w ostatnich n meczach
                          pd.DataFrame(list(map(lambda x: create_aggregate_based_on_variables(x, 3, 'red_card', np.mean), results_split))),
                          pd.DataFrame(list(map(lambda x: create_aggregate_based_on_variables(x, 5, 'red_card', np.mean), results_split))),
                          pd.DataFrame(list(map(lambda x: create_aggregate_based_on_variables(x, 7, 'red_card', np.mean), results_split))),
                          pd.DataFrame(list(map(lambda x: create_aggregate_based_on_variables(x, 3, 'red_card', np.std), results_split))),
                          pd.DataFrame(list(map(lambda x: create_aggregate_based_on_variables(x, 5, 'red_card', np.std), results_split))),
                          pd.DataFrame(list(map(lambda x: create_aggregate_based_on_variables(x, 7, 'red_card', np.std), results_split))),
                          ],axis=1,ignore_index=True)


        

        # Change names of variables
        form_var.columns = ['Team',
                        'pts_avg3','pts_avg5','pts_avg7','pts_std3','pts_std5','pts_std7',
                        'gz_avg3','gz_avg5','gz_avg7','gz_std3','gz_std5','gz_std7',
                        'gs_avg3','gs_avg5','gs_avg7','gs_std3','gs_std5','gs_std7',
                        'sh_od_avg3','sh_od_avg5','sh_od_avg7','sh_od_std3','sh_od_std5','sh_od_std7',
                        'sh_ot_avg3','sh_ot_avg5','sh_ot_avg7','sh_ot_std3','sh_ot_std5','sh_ot_std7',
                        'sot_od_avg3','sot_od_avg5','sot_od_avg7','sot_od_std3','sot_od_std5','sot_od_std7',
                        'sot_ot_avg3','sot_ot_avg5','sot_ot_avg7','sot_ot_std3','sot_ot_std5','sot_ot_std7',
                        'cw_avg3','cw_avg5','cw_avg7','cw_std3','cw_std5','cw_std7',
                        'cb_avg3','cb_avg5','cb_avg7','cb_std3','cb_std5','cb_std7',
                        'yc_avg3','yc_avg5','yc_avg7','yc_std3','yc_std5','yc_std7',
                        'rc_avg3','rc_avg5','rc_avg7','rc_std3','rc_std5','rc_std7'
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

        output_concat = pd.concat([h_var, a_var], axis=1)
        output_concat['position_dst'] = abs(output_concat['h_pozycja'] - output_concat['a_pozycja'])
        return output_concat
    

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

    # save table with courses
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

        # ??? czy to jest nadal potrzebne?
        kursy_concat = pd.DataFrame([[h_kurs,d_kurs,a_kurs]], columns = ['h_course','d_course','a_course'])

        # Line by line, variable for each match are created
        if i == 0:
            calc_features(0, home_team = HOME_TEAM, away_team = AWAY_TEAM).to_csv('vars_to_predict.csv', mode='a', header=True)
        else:
            calc_features(0, home_team = HOME_TEAM, away_team = AWAY_TEAM).to_csv('vars_to_predict.csv', mode='a', header=False)



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
    
    # !Remove courses form returned table - comment this line below if you would like to keep courses
    # courses = courses.drop(['h_course','d_course','a_course'], axis=1)
    

    #######
    # Add a column with information about who will win the match according to the decision tree
    tree_preds = tree_model.predict(preds)
    preds_after_translation = [dicts2translate['idx2str'][elem] for elem in tree_preds]
    courses['prediction'] = preds_after_translation
    courses = courses.round({'pr_h_won': 4, 'pr_draw': 4, 'pr_a_won': 4})

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

