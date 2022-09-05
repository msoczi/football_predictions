
import pandas as pd
import numpy as np
from scipy.stats import linregress
import warnings


def create_agg_var(results):
    
    # Split function
    def split(data, f):
        grouped = data.groupby(f)
        return [g for _, g in grouped], list(grouped.groups.keys())

    results_split, results_split_names = split(results, 'Team')
    # We take the form of the team - different versions are possible here
        
    # Function to measure changes
    def wspolczynnik_zmiennosci(x):
        return np.mean(np.std(x)/np.mean(x))
    
    # Function to show trend
    def trend(x):
        slope, _, _, _, _ = linregress(np.arange(len(x)),x)
        return slope
        
    # Function create aggregate variable 
    def create_aggregate_based_on_variables(team, n, var, stat):
        return stat(team[var][:n])
    
    
    
    with warnings.catch_warnings():
        warnings.simplefilter('ignore')
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
                            pd.DataFrame(list(map(lambda x: create_aggregate_based_on_variables(x, 3, 'pts', trend), results_split))),
                            pd.DataFrame(list(map(lambda x: create_aggregate_based_on_variables(x, 5, 'pts', trend), results_split))),
                            pd.DataFrame(list(map(lambda x: create_aggregate_based_on_variables(x, 7, 'pts', trend), results_split))),
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
                            pd.DataFrame(list(map(lambda x: create_aggregate_based_on_variables(x, 3, 'goal_zdob', trend), results_split))),
                            pd.DataFrame(list(map(lambda x: create_aggregate_based_on_variables(x, 5, 'goal_zdob', trend), results_split))),
                            pd.DataFrame(list(map(lambda x: create_aggregate_based_on_variables(x, 7, 'goal_zdob', trend), results_split))),
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
                            pd.DataFrame(list(map(lambda x: create_aggregate_based_on_variables(x, 3, 'goal_strc', trend), results_split))),
                            pd.DataFrame(list(map(lambda x: create_aggregate_based_on_variables(x, 5, 'goal_strc', trend), results_split))),
                            pd.DataFrame(list(map(lambda x: create_aggregate_based_on_variables(x, 7, 'goal_strc', trend), results_split))),
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
                            pd.DataFrame(list(map(lambda x: create_aggregate_based_on_variables(x, 3, 'sh_odd', trend), results_split))),
                            pd.DataFrame(list(map(lambda x: create_aggregate_based_on_variables(x, 5, 'sh_odd', trend), results_split))),
                            pd.DataFrame(list(map(lambda x: create_aggregate_based_on_variables(x, 7, 'sh_odd', trend), results_split))),
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
                            pd.DataFrame(list(map(lambda x: create_aggregate_based_on_variables(x, 3, 'sh_otrz', trend), results_split))),
                            pd.DataFrame(list(map(lambda x: create_aggregate_based_on_variables(x, 5, 'sh_otrz', trend), results_split))),
                            pd.DataFrame(list(map(lambda x: create_aggregate_based_on_variables(x, 7, 'sh_otrz', trend), results_split))),
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
                            pd.DataFrame(list(map(lambda x: create_aggregate_based_on_variables(x, 3, 'sot_odd', trend), results_split))),
                            pd.DataFrame(list(map(lambda x: create_aggregate_based_on_variables(x, 5, 'sot_odd', trend), results_split))),
                            pd.DataFrame(list(map(lambda x: create_aggregate_based_on_variables(x, 7, 'sot_odd', trend), results_split))),
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
                            pd.DataFrame(list(map(lambda x: create_aggregate_based_on_variables(x, 3, 'sot_otrz', trend), results_split))),
                            pd.DataFrame(list(map(lambda x: create_aggregate_based_on_variables(x, 5, 'sot_otrz', trend), results_split))),
                            pd.DataFrame(list(map(lambda x: create_aggregate_based_on_variables(x, 7, 'sot_otrz', trend), results_split))),
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
                            pd.DataFrame(list(map(lambda x: create_aggregate_based_on_variables(x, 3, 'cor_wyk', trend), results_split))),
                            pd.DataFrame(list(map(lambda x: create_aggregate_based_on_variables(x, 5, 'cor_wyk', trend), results_split))),
                            pd.DataFrame(list(map(lambda x: create_aggregate_based_on_variables(x, 7, 'cor_wyk', trend), results_split))),
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
                            pd.DataFrame(list(map(lambda x: create_aggregate_based_on_variables(x, 3, 'cor_bro', trend), results_split))),
                            pd.DataFrame(list(map(lambda x: create_aggregate_based_on_variables(x, 5, 'cor_bro', trend), results_split))),
                            pd.DataFrame(list(map(lambda x: create_aggregate_based_on_variables(x, 7, 'cor_bro', trend), results_split))),
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
                            pd.DataFrame(list(map(lambda x: create_aggregate_based_on_variables(x, 3, 'yel_card', trend), results_split))),
                            pd.DataFrame(list(map(lambda x: create_aggregate_based_on_variables(x, 5, 'yel_card', trend), results_split))),
                            pd.DataFrame(list(map(lambda x: create_aggregate_based_on_variables(x, 7, 'yel_card', trend), results_split))),
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
                            pd.DataFrame(list(map(lambda x: create_aggregate_based_on_variables(x, 3, 'red_card', trend), results_split))),
                            pd.DataFrame(list(map(lambda x: create_aggregate_based_on_variables(x, 5, 'red_card', trend), results_split))),
                            pd.DataFrame(list(map(lambda x: create_aggregate_based_on_variables(x, 7, 'red_card', trend), results_split))),
                            ],axis=1,ignore_index=True)


    # Change names of variables
    form_var.columns = ['Team',
                            'pts_avg3','pts_avg5','pts_avg7','pts_std3','pts_std5','pts_std7','pts_wz3','pts_wz5','pts_wz7','pts_max3','pts_max5','pts_max7','pts_min3','pts_min5','pts_min7','pts_trd3','pts_trd5','pts_trd7',
                            'gz_avg3','gz_avg5','gz_avg7','gz_std3','gz_std5','gz_std7','gz_wz3','gz_wz5','gz_wz7','gz_max3','gz_max5','gz_max7','gz_min3','gz_min5','gz_min7','gz_trd3','gz_trd5','gz_trd7',
                            'gs_avg3','gs_avg5','gs_avg7','gs_std3','gs_std5','gs_std7','gs_wz3','gs_wz5','gs_wz7','gs_max3','gs_max5','gs_max7','gs_min3','gs_min5','gs_min7','gs_trd3','gs_trd5','gs_trd7',
                            'sh_od_avg3','sh_od_avg5','sh_od_avg7','sh_od_std3','sh_od_std5','sh_od_std7','sh_od_wz3','sh_od_wz5','sh_od_wz7','sh_od_max3','sh_od_max5','sh_od_max7','sh_od_min3','sh_od_min5','sh_od_min7','sh_od_trd3','sh_od_trd5','sh_od_trd7',
                            'sh_ot_avg3','sh_ot_avg5','sh_ot_avg7','sh_ot_std3','sh_ot_std5','sh_ot_std7','sh_ot_wz3','sh_ot_wz5','sh_ot_wz7','sh_ot_max3','sh_ot_max5','sh_ot_max7','sh_ot_min3','sh_ot_min5','sh_ot_min7','sh_ot_trd3','sh_ot_trd5','sh_ot_trd7',
                            'sot_od_avg3','sot_od_avg5','sot_od_avg7','sot_od_std3','sot_od_std5','sot_od_std7','sot_od_wz3','sot_od_wz5','sot_od_wz7','sot_od_max3','sot_od_max5','sot_od_max7','sot_od_min3','sot_od_min5','sot_od_min7','sot_od_trd3','sot_od_trd5','sot_od_trd7',
                            'sot_ot_avg3','sot_ot_avg5','sot_ot_avg7','sot_ot_std3','sot_ot_std5','sot_ot_std7','sot_ot_wz3','sot_ot_wz5','sot_ot_wz7','sot_ot_max3','sot_ot_max5','sot_ot_max7','sot_ot_min3','sot_ot_min5','sot_ot_min7','sot_ot_trd3','sot_ot_trd5','sot_ot_trd7',
                            'cw_avg3','cw_avg5','cw_avg7','cw_std3','cw_std5','cw_std7','cw_wz3','cw_wz5','cw_wz7','cw_max3','cw_max5','cw_max7','cw_min3','cw_min5','cw_min7','cw_trd3','cw_trd5','cw_trd7',
                            'cb_avg3','cb_avg5','cb_avg7','cb_std3','cb_std5','cb_std7','cb_wz3','cb_wz5','cb_wz7','cb_max3','cb_max5','cb_max7','cb_min3','cb_min5','cb_min7','cb_trd3','cb_trd5','cb_trd7',
                            'yc_avg3','yc_avg5','yc_avg7','yc_std3','yc_std5','yc_std7','yc_wz3','yc_wz5','yc_std7','yc_max3','yc_max5','yc_max7','yc_min3','yc_min5','yc_min7','yc_trd3','yc_trd5','yc_trd7',
                            'rc_avg3','rc_avg5','rc_avg7','rc_std3','rc_std5','rc_std7','rc_wz3','rc_wz5','rc_wz7','rc_max3','rc_max5','rc_max7','rc_min3','rc_min5','rc_min7','rc_trd3','rc_trd5','rc_trd7'
                        ]

    form_var = form_var.set_index('Team')
    return form_var
