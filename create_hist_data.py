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
import yaml
import pandas as pd
import numpy as np


N_MATCH_ = int(float(sys.argv[1]))
FILE_READ_ = sys.argv[2]
FILE_SAVE_ = sys.argv[3]


with open("config.yaml", 'r') as configuration:
    config = yaml.safe_load(configuration)


def calc_features(n, file_read):
    def read_data(n, file_read):
        # n=0 - get all rows
        # n=1 - remove 1 row
        # n=k - remove k row
        results = pd.read_csv(file_read, parse_dates=['Date'], dayfirst=True)
        HOME_TEAM = results.iloc[len(results)-1-n].HomeTeam
        AWAY_TEAM = results.iloc[len(results)-1-n].AwayTeam
        match_res = results.iloc[[len(results)-1-n],:][['Date','HomeTeam','AwayTeam','FTR','B365H','B365D','B365A']]
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

    def split(data, f):
        grouped = data.groupby(f)
        return [g for _, g in grouped], list(grouped.groups.keys())

    results_split, results_split_names = split(results, 'Team')
    # We take the form of the team - different versions are possible here
    
    # Function to measure changes
    def wspolczynnik_zmiennosci(x):
        return np.mean(np.std(x)/np.mean(x))
    
    # Function create aggregate variable 
    def create_aggregate_based_on_variables(team, n, var, stat):
        return stat(team[var][:n])

    # Tworzymy zmiene agregaty
    form_var = pd.concat([pd.DataFrame(results_split_names),
                          # Zmiene oparte na liczbie zdobytych punktów w ostatnich n meczach
                          pd.DataFrame(list(map(lambda x: create_aggregate_based_on_variables(x, 3, 'pts', np.mean), results_split))),
                          pd.DataFrame(list(map(lambda x: create_aggregate_based_on_variables(x, 5, 'pts', np.mean), results_split))),
                          pd.DataFrame(list(map(lambda x: create_aggregate_based_on_variables(x, 7, 'pts', np.mean), results_split))),
                          pd.DataFrame(list(map(lambda x: create_aggregate_based_on_variables(x, 3, 'pts', np.std), results_split))),
                          pd.DataFrame(list(map(lambda x: create_aggregate_based_on_variables(x, 5, 'pts', np.std), results_split))),
                          pd.DataFrame(list(map(lambda x: create_aggregate_based_on_variables(x, 7, 'pts', np.std), results_split))),
                          pd.DataFrame(list(map(lambda x: create_aggregate_based_on_variables(x, 3, 'pts', wspolczynnik_zmiennosci), results_split))),
                          pd.DataFrame(list(map(lambda x: create_aggregate_based_on_variables(x, 5, 'pts', wspolczynnik_zmiennosci), results_split))),
                          pd.DataFrame(list(map(lambda x: create_aggregate_based_on_variables(x, 7, 'pts', wspolczynnik_zmiennosci), results_split))),
                          pd.DataFrame(list(map(lambda x: create_aggregate_based_on_variables(x, 3, 'pts', np.max), results_split))),
                          pd.DataFrame(list(map(lambda x: create_aggregate_based_on_variables(x, 5, 'pts', np.max), results_split))),
                          pd.DataFrame(list(map(lambda x: create_aggregate_based_on_variables(x, 7, 'pts', np.max), results_split))),
                          pd.DataFrame(list(map(lambda x: create_aggregate_based_on_variables(x, 3, 'pts', np.min), results_split))),
                          pd.DataFrame(list(map(lambda x: create_aggregate_based_on_variables(x, 5, 'pts', np.min), results_split))),
                          pd.DataFrame(list(map(lambda x: create_aggregate_based_on_variables(x, 7, 'pts', np.min), results_split))),
                          # Zmiene oparte na liczbie zdobytych bramek w ostatnich n meczach
                          pd.DataFrame(list(map(lambda x: create_aggregate_based_on_variables(x, 3, 'goal_zdob', np.mean), results_split))),
                          pd.DataFrame(list(map(lambda x: create_aggregate_based_on_variables(x, 5, 'goal_zdob', np.mean), results_split))),
                          pd.DataFrame(list(map(lambda x: create_aggregate_based_on_variables(x, 7, 'goal_zdob', np.mean), results_split))),
                          pd.DataFrame(list(map(lambda x: create_aggregate_based_on_variables(x, 3, 'goal_zdob', np.std), results_split))),
                          pd.DataFrame(list(map(lambda x: create_aggregate_based_on_variables(x, 5, 'goal_zdob', np.std), results_split))),
                          pd.DataFrame(list(map(lambda x: create_aggregate_based_on_variables(x, 7, 'goal_zdob', np.std), results_split))),
                          pd.DataFrame(list(map(lambda x: create_aggregate_based_on_variables(x, 3, 'goal_zdob', wspolczynnik_zmiennosci), results_split))),
                          pd.DataFrame(list(map(lambda x: create_aggregate_based_on_variables(x, 5, 'goal_zdob', wspolczynnik_zmiennosci), results_split))),
                          pd.DataFrame(list(map(lambda x: create_aggregate_based_on_variables(x, 7, 'goal_zdob', wspolczynnik_zmiennosci), results_split))),
                          pd.DataFrame(list(map(lambda x: create_aggregate_based_on_variables(x, 3, 'goal_zdob', np.max), results_split))),
                          pd.DataFrame(list(map(lambda x: create_aggregate_based_on_variables(x, 5, 'goal_zdob', np.max), results_split))),
                          pd.DataFrame(list(map(lambda x: create_aggregate_based_on_variables(x, 7, 'goal_zdob', np.max), results_split))),
                          pd.DataFrame(list(map(lambda x: create_aggregate_based_on_variables(x, 3, 'goal_zdob', np.min), results_split))),
                          pd.DataFrame(list(map(lambda x: create_aggregate_based_on_variables(x, 5, 'goal_zdob', np.min), results_split))),
                          pd.DataFrame(list(map(lambda x: create_aggregate_based_on_variables(x, 7, 'goal_zdob', np.min), results_split))),
                          # Zmiene oparte na liczbie straconych bramek w ostatnich n meczach
                          pd.DataFrame(list(map(lambda x: create_aggregate_based_on_variables(x, 3, 'goal_strc', np.mean), results_split))),
                          pd.DataFrame(list(map(lambda x: create_aggregate_based_on_variables(x, 5, 'goal_strc', np.mean), results_split))),
                          pd.DataFrame(list(map(lambda x: create_aggregate_based_on_variables(x, 7, 'goal_strc', np.mean), results_split))),
                          pd.DataFrame(list(map(lambda x: create_aggregate_based_on_variables(x, 3, 'goal_strc', np.std), results_split))),
                          pd.DataFrame(list(map(lambda x: create_aggregate_based_on_variables(x, 5, 'goal_strc', np.std), results_split))),
                          pd.DataFrame(list(map(lambda x: create_aggregate_based_on_variables(x, 7, 'goal_strc', np.std), results_split))),
                          pd.DataFrame(list(map(lambda x: create_aggregate_based_on_variables(x, 3, 'goal_strc', wspolczynnik_zmiennosci), results_split))),
                          pd.DataFrame(list(map(lambda x: create_aggregate_based_on_variables(x, 5, 'goal_strc', wspolczynnik_zmiennosci), results_split))),
                          pd.DataFrame(list(map(lambda x: create_aggregate_based_on_variables(x, 7, 'goal_strc', wspolczynnik_zmiennosci), results_split))),
                          pd.DataFrame(list(map(lambda x: create_aggregate_based_on_variables(x, 3, 'goal_strc', np.max), results_split))),
                          pd.DataFrame(list(map(lambda x: create_aggregate_based_on_variables(x, 5, 'goal_strc', np.max), results_split))),
                          pd.DataFrame(list(map(lambda x: create_aggregate_based_on_variables(x, 7, 'goal_strc', np.max), results_split))),
                          pd.DataFrame(list(map(lambda x: create_aggregate_based_on_variables(x, 3, 'goal_strc', np.min), results_split))),
                          pd.DataFrame(list(map(lambda x: create_aggregate_based_on_variables(x, 5, 'goal_strc', np.min), results_split))),
                          pd.DataFrame(list(map(lambda x: create_aggregate_based_on_variables(x, 7, 'goal_strc', np.min), results_split))),
                          # Zmiene oparte na liczbie oddanych strzałów w ostatnich n meczach
                          pd.DataFrame(list(map(lambda x: create_aggregate_based_on_variables(x, 3, 'sh_odd', np.mean), results_split))),
                          pd.DataFrame(list(map(lambda x: create_aggregate_based_on_variables(x, 5, 'sh_odd', np.mean), results_split))),
                          pd.DataFrame(list(map(lambda x: create_aggregate_based_on_variables(x, 7, 'sh_odd', np.mean), results_split))),
                          pd.DataFrame(list(map(lambda x: create_aggregate_based_on_variables(x, 3, 'sh_odd', np.std), results_split))),
                          pd.DataFrame(list(map(lambda x: create_aggregate_based_on_variables(x, 5, 'sh_odd', np.std), results_split))),
                          pd.DataFrame(list(map(lambda x: create_aggregate_based_on_variables(x, 7, 'sh_odd', np.std), results_split))),
                          pd.DataFrame(list(map(lambda x: create_aggregate_based_on_variables(x, 3, 'sh_odd', wspolczynnik_zmiennosci), results_split))),
                          pd.DataFrame(list(map(lambda x: create_aggregate_based_on_variables(x, 5, 'sh_odd', wspolczynnik_zmiennosci), results_split))),
                          pd.DataFrame(list(map(lambda x: create_aggregate_based_on_variables(x, 7, 'sh_odd', wspolczynnik_zmiennosci), results_split))),
                          pd.DataFrame(list(map(lambda x: create_aggregate_based_on_variables(x, 3, 'sh_odd', np.max), results_split))),
                          pd.DataFrame(list(map(lambda x: create_aggregate_based_on_variables(x, 5, 'sh_odd', np.max), results_split))),
                          pd.DataFrame(list(map(lambda x: create_aggregate_based_on_variables(x, 7, 'sh_odd', np.max), results_split))),
                          pd.DataFrame(list(map(lambda x: create_aggregate_based_on_variables(x, 3, 'sh_odd', np.min), results_split))),
                          pd.DataFrame(list(map(lambda x: create_aggregate_based_on_variables(x, 5, 'sh_odd', np.min), results_split))),
                          pd.DataFrame(list(map(lambda x: create_aggregate_based_on_variables(x, 7, 'sh_odd', np.min), results_split))),
                          # Zmiene oparte na liczbie otrzymanych strzałów w ostatnich n meczach
                          pd.DataFrame(list(map(lambda x: create_aggregate_based_on_variables(x, 3, 'sh_otrz', np.mean), results_split))),
                          pd.DataFrame(list(map(lambda x: create_aggregate_based_on_variables(x, 5, 'sh_otrz', np.mean), results_split))),
                          pd.DataFrame(list(map(lambda x: create_aggregate_based_on_variables(x, 7, 'sh_otrz', np.mean), results_split))),
                          pd.DataFrame(list(map(lambda x: create_aggregate_based_on_variables(x, 3, 'sh_otrz', np.std), results_split))),
                          pd.DataFrame(list(map(lambda x: create_aggregate_based_on_variables(x, 5, 'sh_otrz', np.std), results_split))),
                          pd.DataFrame(list(map(lambda x: create_aggregate_based_on_variables(x, 7, 'sh_otrz', np.std), results_split))),
                          pd.DataFrame(list(map(lambda x: create_aggregate_based_on_variables(x, 3, 'sh_otrz', wspolczynnik_zmiennosci), results_split))),
                          pd.DataFrame(list(map(lambda x: create_aggregate_based_on_variables(x, 5, 'sh_otrz', wspolczynnik_zmiennosci), results_split))),
                          pd.DataFrame(list(map(lambda x: create_aggregate_based_on_variables(x, 7, 'sh_otrz', wspolczynnik_zmiennosci), results_split))),
                          pd.DataFrame(list(map(lambda x: create_aggregate_based_on_variables(x, 3, 'sh_otrz', np.max), results_split))),
                          pd.DataFrame(list(map(lambda x: create_aggregate_based_on_variables(x, 5, 'sh_otrz', np.max), results_split))),
                          pd.DataFrame(list(map(lambda x: create_aggregate_based_on_variables(x, 7, 'sh_otrz', np.max), results_split))),
                          pd.DataFrame(list(map(lambda x: create_aggregate_based_on_variables(x, 3, 'sh_otrz', np.min), results_split))),
                          pd.DataFrame(list(map(lambda x: create_aggregate_based_on_variables(x, 5, 'sh_otrz', np.min), results_split))),
                          pd.DataFrame(list(map(lambda x: create_aggregate_based_on_variables(x, 7, 'sh_otrz', np.min), results_split))),
                          # Zmiene oparte na liczbie oddanych strzałów w ostatnich n meczach
                          pd.DataFrame(list(map(lambda x: create_aggregate_based_on_variables(x, 3, 'sot_odd', np.mean), results_split))),
                          pd.DataFrame(list(map(lambda x: create_aggregate_based_on_variables(x, 5, 'sot_odd', np.mean), results_split))),
                          pd.DataFrame(list(map(lambda x: create_aggregate_based_on_variables(x, 7, 'sot_odd', np.mean), results_split))),
                          pd.DataFrame(list(map(lambda x: create_aggregate_based_on_variables(x, 3, 'sot_odd', np.std), results_split))),
                          pd.DataFrame(list(map(lambda x: create_aggregate_based_on_variables(x, 5, 'sot_odd', np.std), results_split))),
                          pd.DataFrame(list(map(lambda x: create_aggregate_based_on_variables(x, 7, 'sot_odd', np.std), results_split))),
                          pd.DataFrame(list(map(lambda x: create_aggregate_based_on_variables(x, 3, 'sot_odd', wspolczynnik_zmiennosci), results_split))),
                          pd.DataFrame(list(map(lambda x: create_aggregate_based_on_variables(x, 5, 'sot_odd', wspolczynnik_zmiennosci), results_split))),
                          pd.DataFrame(list(map(lambda x: create_aggregate_based_on_variables(x, 7, 'sot_odd', wspolczynnik_zmiennosci), results_split))),
                          pd.DataFrame(list(map(lambda x: create_aggregate_based_on_variables(x, 3, 'sot_odd', np.max), results_split))),
                          pd.DataFrame(list(map(lambda x: create_aggregate_based_on_variables(x, 5, 'sot_odd', np.max), results_split))),
                          pd.DataFrame(list(map(lambda x: create_aggregate_based_on_variables(x, 7, 'sot_odd', np.max), results_split))),
                          pd.DataFrame(list(map(lambda x: create_aggregate_based_on_variables(x, 3, 'sot_odd', np.min), results_split))),
                          pd.DataFrame(list(map(lambda x: create_aggregate_based_on_variables(x, 5, 'sot_odd', np.min), results_split))),
                          pd.DataFrame(list(map(lambda x: create_aggregate_based_on_variables(x, 7, 'sot_odd', np.min), results_split))),
                          # Zmiene oparte na liczbie otrzymanych strzałów w ostatnich n meczach
                          pd.DataFrame(list(map(lambda x: create_aggregate_based_on_variables(x, 3, 'sot_otrz', np.mean), results_split))),
                          pd.DataFrame(list(map(lambda x: create_aggregate_based_on_variables(x, 5, 'sot_otrz', np.mean), results_split))),
                          pd.DataFrame(list(map(lambda x: create_aggregate_based_on_variables(x, 7, 'sot_otrz', np.mean), results_split))),
                          pd.DataFrame(list(map(lambda x: create_aggregate_based_on_variables(x, 3, 'sot_otrz', np.std), results_split))),
                          pd.DataFrame(list(map(lambda x: create_aggregate_based_on_variables(x, 5, 'sot_otrz', np.std), results_split))),
                          pd.DataFrame(list(map(lambda x: create_aggregate_based_on_variables(x, 7, 'sot_otrz', np.std), results_split))),
                          pd.DataFrame(list(map(lambda x: create_aggregate_based_on_variables(x, 3, 'sot_otrz', wspolczynnik_zmiennosci), results_split))),
                          pd.DataFrame(list(map(lambda x: create_aggregate_based_on_variables(x, 5, 'sot_otrz', wspolczynnik_zmiennosci), results_split))),
                          pd.DataFrame(list(map(lambda x: create_aggregate_based_on_variables(x, 7, 'sot_otrz', wspolczynnik_zmiennosci), results_split))),
                          pd.DataFrame(list(map(lambda x: create_aggregate_based_on_variables(x, 3, 'sot_otrz', np.max), results_split))),
                          pd.DataFrame(list(map(lambda x: create_aggregate_based_on_variables(x, 5, 'sot_otrz', np.max), results_split))),
                          pd.DataFrame(list(map(lambda x: create_aggregate_based_on_variables(x, 7, 'sot_otrz', np.max), results_split))),
                          pd.DataFrame(list(map(lambda x: create_aggregate_based_on_variables(x, 3, 'sot_otrz', np.min), results_split))),
                          pd.DataFrame(list(map(lambda x: create_aggregate_based_on_variables(x, 5, 'sot_otrz', np.min), results_split))),
                          pd.DataFrame(list(map(lambda x: create_aggregate_based_on_variables(x, 7, 'sot_otrz', np.min), results_split))),
                          # Zmiene oparte na liczbie kornerów wykonanych w ostatnich n meczach
                          pd.DataFrame(list(map(lambda x: create_aggregate_based_on_variables(x, 3, 'cor_wyk', np.mean), results_split))),
                          pd.DataFrame(list(map(lambda x: create_aggregate_based_on_variables(x, 5, 'cor_wyk', np.mean), results_split))),
                          pd.DataFrame(list(map(lambda x: create_aggregate_based_on_variables(x, 7, 'cor_wyk', np.mean), results_split))),
                          pd.DataFrame(list(map(lambda x: create_aggregate_based_on_variables(x, 3, 'cor_wyk', np.std), results_split))),
                          pd.DataFrame(list(map(lambda x: create_aggregate_based_on_variables(x, 5, 'cor_wyk', np.std), results_split))),
                          pd.DataFrame(list(map(lambda x: create_aggregate_based_on_variables(x, 7, 'cor_wyk', np.std), results_split))),
                          pd.DataFrame(list(map(lambda x: create_aggregate_based_on_variables(x, 3, 'cor_wyk', wspolczynnik_zmiennosci), results_split))),
                          pd.DataFrame(list(map(lambda x: create_aggregate_based_on_variables(x, 5, 'cor_wyk', wspolczynnik_zmiennosci), results_split))),
                          pd.DataFrame(list(map(lambda x: create_aggregate_based_on_variables(x, 7, 'cor_wyk', wspolczynnik_zmiennosci), results_split))),
                          pd.DataFrame(list(map(lambda x: create_aggregate_based_on_variables(x, 3, 'cor_wyk', np.max), results_split))),
                          pd.DataFrame(list(map(lambda x: create_aggregate_based_on_variables(x, 5, 'cor_wyk', np.max), results_split))),
                          pd.DataFrame(list(map(lambda x: create_aggregate_based_on_variables(x, 7, 'cor_wyk', np.max), results_split))),
                          pd.DataFrame(list(map(lambda x: create_aggregate_based_on_variables(x, 3, 'cor_wyk', np.min), results_split))),
                          pd.DataFrame(list(map(lambda x: create_aggregate_based_on_variables(x, 5, 'cor_wyk', np.min), results_split))),
                          pd.DataFrame(list(map(lambda x: create_aggregate_based_on_variables(x, 7, 'cor_wyk', np.min), results_split))),
                          # Zmiene oparte na liczbie korneró bronionych w ostatnich n meczach
                          pd.DataFrame(list(map(lambda x: create_aggregate_based_on_variables(x, 3, 'cor_bro', np.mean), results_split))),
                          pd.DataFrame(list(map(lambda x: create_aggregate_based_on_variables(x, 5, 'cor_bro', np.mean), results_split))),
                          pd.DataFrame(list(map(lambda x: create_aggregate_based_on_variables(x, 7, 'cor_bro', np.mean), results_split))),
                          pd.DataFrame(list(map(lambda x: create_aggregate_based_on_variables(x, 3, 'cor_bro', np.std), results_split))),
                          pd.DataFrame(list(map(lambda x: create_aggregate_based_on_variables(x, 5, 'cor_bro', np.std), results_split))),
                          pd.DataFrame(list(map(lambda x: create_aggregate_based_on_variables(x, 7, 'cor_bro', np.std), results_split))),
                          pd.DataFrame(list(map(lambda x: create_aggregate_based_on_variables(x, 3, 'cor_bro', wspolczynnik_zmiennosci), results_split))),
                          pd.DataFrame(list(map(lambda x: create_aggregate_based_on_variables(x, 5, 'cor_bro', wspolczynnik_zmiennosci), results_split))),
                          pd.DataFrame(list(map(lambda x: create_aggregate_based_on_variables(x, 7, 'cor_bro', wspolczynnik_zmiennosci), results_split))),
                          pd.DataFrame(list(map(lambda x: create_aggregate_based_on_variables(x, 3, 'cor_bro', np.max), results_split))),
                          pd.DataFrame(list(map(lambda x: create_aggregate_based_on_variables(x, 5, 'cor_bro', np.max), results_split))),
                          pd.DataFrame(list(map(lambda x: create_aggregate_based_on_variables(x, 7, 'cor_bro', np.max), results_split))),
                          pd.DataFrame(list(map(lambda x: create_aggregate_based_on_variables(x, 3, 'cor_bro', np.min), results_split))),
                          pd.DataFrame(list(map(lambda x: create_aggregate_based_on_variables(x, 5, 'cor_bro', np.min), results_split))),
                          pd.DataFrame(list(map(lambda x: create_aggregate_based_on_variables(x, 7, 'cor_bro', np.min), results_split))),
                          # Zmiene oparte na liczbie zółtych kartek w ostatnich n meczach
                          pd.DataFrame(list(map(lambda x: create_aggregate_based_on_variables(x, 3, 'yel_card', np.mean), results_split))),
                          pd.DataFrame(list(map(lambda x: create_aggregate_based_on_variables(x, 5, 'yel_card', np.mean), results_split))),
                          pd.DataFrame(list(map(lambda x: create_aggregate_based_on_variables(x, 7, 'yel_card', np.mean), results_split))),
                          pd.DataFrame(list(map(lambda x: create_aggregate_based_on_variables(x, 3, 'yel_card', np.std), results_split))),
                          pd.DataFrame(list(map(lambda x: create_aggregate_based_on_variables(x, 5, 'yel_card', np.std), results_split))),
                          pd.DataFrame(list(map(lambda x: create_aggregate_based_on_variables(x, 7, 'yel_card', np.std), results_split))),
                          pd.DataFrame(list(map(lambda x: create_aggregate_based_on_variables(x, 3, 'yel_card', wspolczynnik_zmiennosci), results_split))),
                          pd.DataFrame(list(map(lambda x: create_aggregate_based_on_variables(x, 5, 'yel_card', wspolczynnik_zmiennosci), results_split))),
                          pd.DataFrame(list(map(lambda x: create_aggregate_based_on_variables(x, 7, 'yel_card', wspolczynnik_zmiennosci), results_split))),
                          pd.DataFrame(list(map(lambda x: create_aggregate_based_on_variables(x, 3, 'yel_card', np.max), results_split))),
                          pd.DataFrame(list(map(lambda x: create_aggregate_based_on_variables(x, 5, 'yel_card', np.max), results_split))),
                          pd.DataFrame(list(map(lambda x: create_aggregate_based_on_variables(x, 7, 'yel_card', np.max), results_split))),
                          pd.DataFrame(list(map(lambda x: create_aggregate_based_on_variables(x, 3, 'yel_card', np.min), results_split))),
                          pd.DataFrame(list(map(lambda x: create_aggregate_based_on_variables(x, 5, 'yel_card', np.min), results_split))),
                          pd.DataFrame(list(map(lambda x: create_aggregate_based_on_variables(x, 7, 'yel_card', np.min), results_split))),
                          # Zmiene oparte na liczbie czerwonych kartek w ostatnich n meczach
                          pd.DataFrame(list(map(lambda x: create_aggregate_based_on_variables(x, 3, 'red_card', np.mean), results_split))),
                          pd.DataFrame(list(map(lambda x: create_aggregate_based_on_variables(x, 5, 'red_card', np.mean), results_split))),
                          pd.DataFrame(list(map(lambda x: create_aggregate_based_on_variables(x, 7, 'red_card', np.mean), results_split))),
                          pd.DataFrame(list(map(lambda x: create_aggregate_based_on_variables(x, 3, 'red_card', np.std), results_split))),
                          pd.DataFrame(list(map(lambda x: create_aggregate_based_on_variables(x, 5, 'red_card', np.std), results_split))),
                          pd.DataFrame(list(map(lambda x: create_aggregate_based_on_variables(x, 7, 'red_card', np.std), results_split))),
                          pd.DataFrame(list(map(lambda x: create_aggregate_based_on_variables(x, 3, 'red_card', wspolczynnik_zmiennosci), results_split))),
                          pd.DataFrame(list(map(lambda x: create_aggregate_based_on_variables(x, 5, 'red_card', wspolczynnik_zmiennosci), results_split))),
                          pd.DataFrame(list(map(lambda x: create_aggregate_based_on_variables(x, 7, 'red_card', wspolczynnik_zmiennosci), results_split))),
                          pd.DataFrame(list(map(lambda x: create_aggregate_based_on_variables(x, 3, 'red_card', np.max), results_split))),
                          pd.DataFrame(list(map(lambda x: create_aggregate_based_on_variables(x, 5, 'red_card', np.max), results_split))),
                          pd.DataFrame(list(map(lambda x: create_aggregate_based_on_variables(x, 7, 'red_card', np.max), results_split))),
                          pd.DataFrame(list(map(lambda x: create_aggregate_based_on_variables(x, 3, 'red_card', np.min), results_split))),
                          pd.DataFrame(list(map(lambda x: create_aggregate_based_on_variables(x, 5, 'red_card', np.min), results_split))),
                          pd.DataFrame(list(map(lambda x: create_aggregate_based_on_variables(x, 7, 'red_card', np.min), results_split))),
                          ],axis=1,ignore_index=True)

    # Nazywamy zmienne
    form_var.columns = ['Team',
                        'pts_avg3','pts_avg5','pts_avg7','pts_std3','pts_std5','pts_std7','pts_wz3','pts_wz5','pts_wz7','pts_max3','pts_max5','pts_max7','pts_min3','pts_min5','pts_min7',
                        'gz_avg3','gz_avg5','gz_avg7','gz_std3','gz_std5','gz_std7','gz_wz3','gz_wz5','gz_wz7','gz_max3','gz_max5','gz_max7','gz_min3','gz_min5','gz_min7',
                        'gs_avg3','gs_avg5','gs_avg7','gs_std3','gs_std5','gs_std7','gs_wz3','gs_wz5','gs_wz7','gs_max3','gs_max5','gs_max7','gs_min3','gs_min5','gs_min7',
                        'sh_od_avg3','sh_od_avg5','sh_od_avg7','sh_od_std3','sh_od_std5','sh_od_std7','sh_od_wz3','sh_od_wz5','sh_od_wz7','sh_od_max3','sh_od_max5','sh_od_max7','sh_od_min3','sh_od_min5','sh_od_min7',
                        'sh_ot_avg3','sh_ot_avg5','sh_ot_avg7','sh_ot_std3','sh_ot_std5','sh_ot_std7','sh_ot_wz3','sh_ot_wz5','sh_ot_wz7','sh_ot_max3','sh_ot_max5','sh_ot_max7','sh_ot_min3','sh_ot_min5','sh_ot_min7',
                        'sot_od_avg3','sot_od_avg5','sot_od_avg7','sot_od_std3','sot_od_std5','sot_od_std7','sot_od_wz3','sot_od_wz5','sot_od_wz7','sot_od_max3','sot_od_max5','sot_od_max7','sot_od_min3','sot_od_min5','sot_od_min7',
                        'sot_ot_avg3','sot_ot_avg5','sot_ot_avg7','sot_ot_std3','sot_ot_std5','sot_ot_std7','sot_ot_wz3','sot_ot_wz5','sot_ot_wz7','sot_ot_max3','sot_ot_max5','sot_ot_max7','sot_ot_min3','sot_ot_min5','sot_ot_min7',
                        'cw_avg3','cw_avg5','cw_avg7','cw_std3','cw_std5','cw_std7','cw_wz3','cw_wz5','cw_wz7','cw_max3','cw_max5','cw_max7','cw_min3','cw_min5','cw_min7',
                        'cb_avg3','cb_avg5','cb_avg7','cb_std3','cb_std5','cb_std7','cb_wz3','cb_wz5','cb_wz7','cb_max3','cb_max5','cb_max7','cb_min3','cb_min5','cb_min7',
                        'yc_avg3','yc_avg5','yc_avg7','yc_std3','yc_std5','yc_std7','yc_wz3','yc_wz5','yc_std7','yc_max3','yc_max5','yc_max7','yc_min3','yc_min5','yc_min7',
                        'rc_avg3','rc_avg5','rc_avg7','rc_std3','rc_std5','rc_std7','rc_wz3','rc_wz5','rc_wz7','rc_max3','rc_max5','rc_max7','rc_min3','rc_min5','rc_min7'
                       ]

    form_var = form_var.set_index('Team')

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

    ###########################################################################
    # The (almost) output table - data with created variables
    ###########################################################################

    output = pd.concat([form_var,
                        res_table[['pts_per_math','gz','gs','sh_od','sh_ot','cw','cb','pozycja']]
                       ], axis=1)
    
    h_var = output.loc[[HOME_TEAM] , : ]
    h_var.columns = ['h_'+i for i in h_var.columns]
    h_var.index = [0]

    a_var = output.loc[[AWAY_TEAM] , : ]
    a_var.columns = ['a_'+i for i in a_var.columns]
    a_var.index = [0]
    
    output_concat = pd.concat([match_res, h_var, a_var], axis=1)
    output_concat['position_dst'] = abs(output_concat['h_pozycja'] - output_concat['a_pozycja'])
    
    output_concat = output_concat.rename(columns={"B365H": "h_course", "B365D": "d_course", "B365A":"a_course"})

    return output_concat




###########################################################################################################################
###########################################################################################################################
###########################################################################################################################


# Check number of matches - argument to main fuction to pass
# calc_features(378, file_read='SP1.csv')


# Save data to .csv - variables for each pair of teams in specific match
def create_hist_data(N_match, file_read, file_save):
    calc_features(N_match, file_read=file_read).to_csv(file_save, index=False)
    for i in range(0,N_match):
        print(f'Save: {i+1}/{N_match}')
        calc_features(N_match-1-i, file_read=file_read).to_csv(file_save, mode='a', header=False, index=False)


# Run main function
#create_hist_data(378, 'SP1.csv', 'hist_data.csv')
create_hist_data(N_MATCH_, FILE_READ_, FILE_SAVE_)

# LOG
print('File saved successfully!')
