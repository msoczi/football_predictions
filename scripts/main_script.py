# LOG
print('Read modules...')

import sys
sys.path.append('scripts//components//')

import yaml
import os
import re
import pandas as pd
import numpy as np
import requests
import warnings
from bs4 import BeautifulSoup
from datetime import datetime
import xgboost as xgb
from sklearn.tree import DecisionTreeClassifier
import pickle

import time

# import own components
from aggvarfun import create_agg_var




LEAGUE = str(sys.argv[1])


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
    #if league == 'PremierLeague':
    #    req = requests.get('https://www.football-data.co.uk/mmz4281/'+config['season']+'/E0.csv')
    #if league == 'Bundesliga':
    #    req = requests.get('https://www.football-data.co.uk/mmz4281/'+config['season']+'/D1.csv')
    #if league == 'SerieA':
    #    req = requests.get('https://www.football-data.co.uk/mmz4281/'+config['season']+'/I1.csv')
    #if league == 'LaLiga':
    #    req = requests.get('https://www.football-data.co.uk/mmz4281/'+config['season']+'/SP1.csv')
        
    req = requests.get('https://www.football-data.co.uk/mmz4281/'+config['season']+config['csv_name'][league])
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
            """
            Function read data form E0.csv file, drop n last rows and return a truncated DataFrame.
            # n=0 - keep all rows
            # n=1 - remove 1 row
            # n=k - remove k row
            """
            results = pd.read_csv('E0.csv', parse_dates=['Date'], dayfirst=True)
            results = results.drop(results.tail(n+1).index)
            return results

        results = read_data(0)
        results = results[['Date','HomeTeam','AwayTeam','FTHG','FTAG','FTR','HS','AS','HST','AST','HC','AC','HY','AY','HR','AR']]
        table = pd.DataFrame(set(results.HomeTeam), columns = ['Team'])  # is this still necessary??
        
        results2 = results.copy()
        results2 = results2.drop(['HomeTeam'], axis=1)
        results2['HomeTeam'] = results2.AwayTeam
        results2 = results2.drop(['AwayTeam'], axis=1)
        results2['HoA'] = 'A'
        results['HoA'] = 'H'
        results = results.drop(['AwayTeam'], axis=1)
        # Tables:
        # results - statistics from the home team point of view
        # results2 - statistics from the away team point of view
        
        # Concat results and results2 to have statisctis from both (home and away) point of view - to create variables relating to a specific match
        results = pd.concat([results, results2], axis=0,ignore_index=True)
        results.rename(columns={'HomeTeam':'Team'}, inplace=True)
        #results['Date'] = pd.to_datetime(results['Date'], format='%d/%m/%y')
        results = results.sort_values(by=['Date'], ascending=False)
        
        
        #############################################################
        ### Create variables relating to a specific match
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
        ### END OF create variables relating to a specific match
        #############################################################



        ##################################################
        ### Create variables-aggregates (in time)
        
        # Preparing data for create those variables-aggregates:
        # - split() will create DataFrame with all matches (sorted decreasing in time) for each team.
        # - then for each Team we can create time-based variable e.g. number of goals scored in last 3 matches
        # - then, there will be created table 'form_var' with variables-aggregates for each teams

        form_var = create_agg_var(results=results)
        
        ### END OF create variables-aggregates (in time)
        ##################################################
        
        
        
        

        #####################################################################
        ### Create a league table and other variables (based on league table)
        # - here we will create a league table based on DataFrame with all matches
        # - we will aggregate simple statistics like 'shots on target' to create variables like 'sum of shots on target in whole season so far'

        # Read matches with drop n rows
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
        
        ### END OF Create a league table and other variables (based on league table)
        #####################################################################
        
        
        ####################################################################################
        # Get fifa team ratings
        fifa_rating_df = pd.read_csv(f"model\\fifa_ratings\\fifa_rating_{LEAGUE}_{config['season'][:2]}.csv", sep=';')
        fifa_rating_df = fifa_rating_df.set_index('Name')


        ###########################################################################
        ### Concatenate tables with all types of variables:
        # - form_var (aggregates)
        # - res_table (variables from league table)
        # - fifa_rating_df (FIFA ratings teams)
        # The (almost) output table is the data with created variables
        ###########################################################################

        output = pd.concat([form_var,
                            res_table[['pts_per_math','gz','gs','sh_od','sh_ot','cw','cb','pozycja']],
                            fifa_rating_df
                           ], axis=1)

        h_var = output.loc[[home_team] , : ]
        h_var.columns = ['h_'+i for i in h_var.columns]
        h_var.index = [0]

        a_var = output.loc[[away_team] , : ]
        a_var.columns = ['a_'+i for i in a_var.columns]
        a_var.index = [0]

        output_concat = pd.concat([h_var, a_var], axis=1)
        output_concat['position_dst'] = abs(output_concat['h_pozycja'] - output_concat['a_pozycja'])
        output_concat['ATT_dst'] = abs(output_concat['h_ATT'] - output_concat['a_ATT'])
        output_concat['MID_dst'] = abs(output_concat['h_MID'] - output_concat['a_MID'])
        output_concat['DEF_dst'] = abs(output_concat['h_DEF'] - output_concat['a_DEF'])
        output_concat['OVR_dst'] = abs(output_concat['h_OVR'] - output_concat['a_OVR'])
        return output_concat
    




    ####################################################################################
    # Scraping future matches and their odds from the STS website
    def odds_scraping():
        page = requests.get(config['scraping'][league])
        soup = BeautifulSoup(page.content, 'html.parser')
        
        scraping_teams = soup.findAll("div", { "class" : "fixres__item"})
        
        scraping_home_teams = []
        scraping_away_teams = []
        for i in range(20): # number of upcoming matches
            scraping_home_teams.append(scraping_teams[i].findAll("span", { "class" : "swap-text__target"})[0].text)
            scraping_away_teams.append(scraping_teams[i].findAll("span", { "class" : "swap-text__target"})[1].text)
        
        del scraping_teams
        scraping_matches = pd.DataFrame([scraping_home_teams, scraping_away_teams]).T
        scraping_matches.columns = ['HomeTeam','AwayTeam']
        
        return scraping_matches
    
    # Call function to create DataFrame 'scraping_matches' with odds
    scraping_matches = odds_scraping()





    ####################################################################################
    # Creating a vars_to_predict file with created variables for a given team
    teams_names_dict = config['teams_names_dict'][league]
    
    
    # setup toolbar
    toolbar_width = len(scraping_matches)
    sys.stdout.write("Progress: [%s]" % (" " * toolbar_width))
    sys.stdout.flush()
    sys.stdout.write("\b" * (toolbar_width+1)) # return to start of line, after '['
    
    for i in range(len(scraping_matches)):
        HOME_TEAM = teams_names_dict[scraping_matches.iloc[i,0]]
        AWAY_TEAM = teams_names_dict[scraping_matches.iloc[i,1]]

        # Line by line, variable for each match are created
        if i == 0:
            calc_features(0, home_team = HOME_TEAM, away_team = AWAY_TEAM).to_csv('vars_to_predict.csv', mode='a', header=True)
        else:
            calc_features(0, home_team = HOME_TEAM, away_team = AWAY_TEAM).to_csv('vars_to_predict.csv', mode='a', header=False)
        
        # update the bar
        sys.stdout.write("-")
        sys.stdout.flush()
    
    # this ends the progress bar
    sys.stdout.write("]\n")


    ####################################################################################
    # Prediction and summary result 
    data_to_predict = pd.read_csv('vars_to_predict.csv', sep=',')
    data_to_predict = data_to_predict.drop(['Unnamed: 0'], axis=1)

    scraping_matches = scraping_matches[['HomeTeam','AwayTeam']]

    # Uploading models and components
    xgb_model = pickle.load(open('model\\xgb_model.pkl', "rb"))
    tree_model = pickle.load(open('model\\tree_model.pkl', "rb"))
    dicts2translate = pickle.load(open('model\\dicts2translate.pkl', "rb"))

    # Prediction
    #data_to_predict = xgb.DMatrix(data_to_predict)   # only when use xgb.train insted of XGBClasiffier
    preds = pd.DataFrame(xgb_model.predict_proba(data_to_predict))
    
    scraping_matches['pr_h_won'] = preds[0]
    scraping_matches['pr_draw']  = preds[1]
    scraping_matches['pr_a_won'] = preds[2]
    
    # !Remove courses form returned table - comment this line below if you would like to keep courses
    # courses = courses.drop(['h_course','d_course','a_course'], axis=1)
    

    #######
    # Add a column with information about who will win the match according to the decision tree
    tree_preds = tree_model.predict(preds)
    preds_after_translation = [dicts2translate['idx2str'][elem] for elem in tree_preds]
    scraping_matches['prediction'] = preds_after_translation
    scraping_matches = scraping_matches.round({'pr_h_won': 2, 'pr_draw': 2, 'pr_a_won': 2})
    scraping_matches.columns = ['Home','Away','P(H)','P(D)','P(A)','Prediction']

    # Remove unnecessary temporary files
    os.remove('vars_to_predict.csv')
    os.remove('E0.csv')

    return scraping_matches
    

# LOG
print('Predictions for',LEAGUE, 'in progress...')

# Run function for premier league
scraping_matches = predict_results(league = LEAGUE)

# Save output in .md file
#with open('output.md', 'w') as file:
#    file.write(scraping_matches.to_markdown(index = False))
# Save output in html file
with open('output_tables/'+LEAGUE+'.html', 'w') as file:
    file.write(scraping_matches.to_html(index = False, classes='content-table', justify='center'))

# LOG
print(f'Process complited!\n Output in: output_tables/{LEAGUE}.html')

