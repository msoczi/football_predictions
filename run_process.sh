#!/bin/bash
python main_script.py PremierLeague
python main_script.py Bundesliga
python main_script.py SerieA
python main_script.py LaLiga
python main_script.py Ligue1

python prepare_index_html.py

python edit_index_html.py PremierLeague
python edit_index_html.py Bundesliga
python edit_index_html.py SerieA
python edit_index_html.py LaLiga
python edit_index_html.py Ligue1

