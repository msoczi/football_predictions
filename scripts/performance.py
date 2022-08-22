
import sys
import yaml
import pandas as pd
import numpy as np
import pickle

import xgboost as xgb
from sklearn.tree import DecisionTreeClassifier

from sklearn.metrics import confusion_matrix
from sklearn import tree # czy to naprawde potrzebne?

from sklearn.metrics import classification_report

from matplotlib import pyplot as plt
from seaborn import heatmap


# -----------------------
# ARGUMENTS
FILE_NAME_ = str(sys.argv[1])
# -----------------------




# ---------------------------------------------
# Read config file
with open("config.yaml", 'r') as configuration:
    config = yaml.safe_load(configuration)

# Read data - csv output from create_hist_data.py script
data = pd.read_csv(FILE_NAME_, sep=',')
y_true = data.FTR
data = data.drop(['FTR','Date','HomeTeam','AwayTeam','h_course','d_course','a_course'], axis=1)
# ---------------------------------------------





# -----------------------------------------------------------
# READ MODEL COMPONENTS
# Uploading models and components
xgb_model = pickle.load(open('model\\xgb_model.pkl', "rb"))
tree_model = pickle.load(open('model\\tree_model.pkl', "rb"))
dicts2translate = pickle.load(open('model\\dicts2translate.pkl', "rb"))
# -----------------------------------------------------------





# ---------------------------------------------------------------------
# Prediction
preds = pd.DataFrame(xgb_model.predict_proba(data))

pred_df = pd.DataFrame()
pred_df['pr_h_won'] = preds[0]
pred_df['pr_draw']  = preds[1]
pred_df['pr_a_won'] = preds[2]

# Add a column with information about who will win the match according to the decision tree
tree_preds = tree_model.predict(preds)
preds_after_translation = [dicts2translate['idx2str'][elem] for elem in tree_preds]
pred_df['prediction'] = preds_after_translation
pred_df = pred_df.round({'pr_h_won': 4, 'pr_draw': 4, 'pr_a_won': 4})
# ---------------------------------------------------------------------



# Print classification report
print(classification_report(y_true, pred_df.prediction))


# EXAMPLE:
# python performance.py hist_PremierLeague.csv
