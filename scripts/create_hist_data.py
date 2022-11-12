############################################################
################### CREATE HISTORIC DATA ###################
############################################################
## Tool for reading the table and removing the last rows  ##
## one by one to create historical data.                  ##
############################################################
####################### INSTRUCTIONS #######################
### To generate historical data:
### 1) get data from www.football-data.co.uk and ensure that there are necessary columns
### 2) tune argument of function calc_features() to create dataset with variables (max possible )
### 3) run this script



import sys
sys.path.append('scripts//components//')

import yaml
import pandas as pd
import numpy as np
from scipy.stats import linregress
import requests
from bs4 import BeautifulSoup

# import own components
from aggvarfun import create_agg_var


N_MATCH_ = int(float(sys.argv[1]))
FILE_READ_ = sys.argv[2]
FILE_SAVE_ = sys.argv[3]
LEAGUE_ = sys.argv[4]


with open("config.yaml", 'r') as configuration:
    config = yaml.safe_load(configuration)


def calc_features(n, file_read, league):
    def read_data(n, file_read):
        # n=0 - get all rows
        # n=1 - remove 1 row
        # n=k - remove k row
        results = pd.read_csv(file_read, parse_dates=['Date'], dayfirst=True)
        HOME_TEAM = results.iloc[len(results)-1-n].HomeTeam
        AWAY_TEAM = results.iloc[len(results)-1-n].AwayTeam
        match_res = results.iloc[[len(results)-1-n],:][['Date','HomeTeam','AwayTeam','FTHG','FTAG','FTR','B365H','B365D','B365A']]
        match_res.index = [0]
        results = results.drop(results.tail(n+1).index)
        return HOME_TEAM, AWAY_TEAM, match_res, results

    # Przygotowanie podstawowych statystyk dotyczacych zespolow
    HOME_TEAM, AWAY_TEAM, match_res, results = read_data(0, file_read)
    results = results[['Date','HomeTeam','AwayTeam','FTHG','FTAG','FTR','B365H','B365D','B365A','HS','AS','HST','AST','HC','AC','HY','AY','HR','AR']]
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

    # Tworzenie podstawowych zmiennychopartych na podstawowych statystykach
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
    form_var = create_agg_var(results=results)
    
    
    
    
    ###################################################################
    # Create a league table and other variables (not based on time)
    ###################################################################

    HOME_TEAM, AWAY_TEAM, match_res, results = read_data(n, file_read)
    results = results[['Date','HomeTeam','AwayTeam','FTHG','FTAG','FTR','HS','AS','HST','AST','HC','AC']]
    #table = pd.DataFrame(set(results.HomeTeam), columns = ['Team'])

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



    ####################################################################################
    # Scraping future matches and their odds from the STS website
    def fifa_rating_scraping(config=config):
            page = requests.get(f'https://www.fifaindex.com/teams/fifa'+config['season'][:2]+'/?league='+config['fifa_rating_league_no'][LEAGUE_])
            soup = BeautifulSoup(page.content, 'html.parser')
            
            table = soup.findAll("table", { "class" : "table table-striped table-teams"})

            fifa_rating_df = pd.read_html(str(table))[0].dropna(axis=0, how='all').dropna(axis=1, how='all').reset_index(drop=True)[['Name','ATT','MID','DEF','OVR']]
            
            fifa_rating_df = fifa_rating_df.replace({"Name": config['fifa_rating_teams_dict'][LEAGUE_]})
            fifa_rating_df = fifa_rating_df.set_index('Name')
            return fifa_rating_df
        
    # Call function to create DataFrame 'courses' with odds
    fifa_rating_df = fifa_rating_scraping()



    ###########################################################################
    # The (almost) output table - data with created variables
    ###########################################################################

    output = pd.concat([form_var,
                        res_table[['pts_per_math','gz','gs','sh_od','sh_ot','cw','cb','pozycja']],
                        fifa_rating_df
                       ], axis=1)
    
    h_var = output.loc[[HOME_TEAM] , : ]
    h_var.columns = ['h_'+i for i in h_var.columns]
    h_var.index = [0]

    a_var = output.loc[[AWAY_TEAM] , : ]
    a_var.columns = ['a_'+i for i in a_var.columns]
    a_var.index = [0]
    
    output_concat = pd.concat([match_res, h_var, a_var], axis=1)
    output_concat['position_dst'] = abs(output_concat['h_pozycja'] - output_concat['a_pozycja'])
    output_concat['ATT_dst'] = abs(output_concat['h_ATT'] - output_concat['a_ATT'])
    output_concat['MID_dst'] = abs(output_concat['h_MID'] - output_concat['a_MID'])
    output_concat['DEF_dst'] = abs(output_concat['h_DEF'] - output_concat['a_DEF'])
    output_concat['OVR_dst'] = abs(output_concat['h_OVR'] - output_concat['a_OVR'])
    
    output_concat = output_concat.rename(columns={"B365H": "h_course", "B365D": "d_course", "B365A":"a_course"})

    return output_concat




###########################################################################################################################
###########################################################################################################################
###########################################################################################################################


# Check number of matches - argument to main fuction to pass
# calc_features(378, file_read='SP1.csv')


# Save data to .csv - variables for each pair of teams in specific match
def create_hist_data(N_match, file_read, file_save):
    calc_features(N_match, file_read=file_read, league=LEAGUE_).to_csv(file_save, index=False)
    for i in range(0,N_match):
        print(f'Save: {i+1}/{N_match}')
        calc_features(N_match-1-i, file_read=file_read, league=LEAGUE_).to_csv(file_save, mode='a', header=False, index=False)


# Run main function
#create_hist_data(378, 'SP1.csv', 'hist_data.csv')
create_hist_data(N_MATCH_, FILE_READ_, FILE_SAVE_)

# LOG
print('File saved successfully!')
