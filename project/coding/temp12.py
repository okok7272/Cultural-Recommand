import pandas as pd
import numpy as np
import pickle
import sqlite3

from sklearn.model_selection import train_test_split
from category_encoders import TargetEncoder
from sklearn.feature_selection import f_regression, SelectKBest
from sklearn.impute import SimpleImputer
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_val_score
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import RandomizedSearchCV
from scipy.stats import randint, uniform

dbpath = 'project\culture.db'

conn = sqlite3.connect(dbpath)
cur = conn.cursor()
culture = pd.read_sql("SELECT * FROM cultural;",conn, index_col=None)

# culture = pd.read_sql("SELECT * FROM outdoor;",conn, index_col=None)

# def errorcode( x):
#   if(x == "오픈런"):
#     x="2024.12.31."
#   return x
# culture['end_period']= culture['end_period'].apply(errorcode)
# culture['end_period']= culture['end_period'].str.rstrip('.')
# culture['start_period']=culture['start_period'].str.rstrip('.')

# culture[['syear','smonth','sday']]= culture['start_period'].str.split('.',expand=True)
# culture[['eyear','emonth','eday']]= culture['end_period'].str.split('.',expand=True)
# culture[['syear','smonth','sday']]= culture[['syear','smonth','sday']].apply(pd.to_numeric)
# culture[['eyear','emonth','eday']]= culture[['eyear','emonth','eday']].apply(pd.to_numeric)

culture = culture.drop(columns=['start_period', 'end_period'])

culcsv = culture.copy()
train = culcsv.copy()

target = 'region_number'

X_train = train.drop(columns=target)

sqlcon = sqlite3.connect('project/culture.db')
X_train.to_sql('traindata',sqlcon)