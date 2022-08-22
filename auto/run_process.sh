#!/bin/bash
python scripts//main_script.py PremierLeague
python scripts//main_script.py Bundesliga
python scripts//main_script.py SerieA
python scripts//main_script.py LaLiga
python scripts//main_script.py Ligue1

python scripts//prepare_index_html.py

python scripts//edit_index_html.py PremierLeague
python scripts//edit_index_html.py Bundesliga
python scripts//edit_index_html.py SerieA
python scripts//edit_index_html.py LaLiga
python scripts//edit_index_html.py Ligue1

