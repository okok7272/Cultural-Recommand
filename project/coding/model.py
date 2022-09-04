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
culture = pd.read_sql("SELECT * FROM outdoor;",conn, index_col=None)

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

target = 'door'
train, val = train_test_split(train ,train_size=0.80,test_size = 0.20, stratify=train[target],random_state=2)

X_train = train.drop(columns=target)
y_train = train[target]
X_val = val.drop(columns=target)
y_val = val[target]

pipe = make_pipeline(
    # TargetEncoder: 범주형 변수 인코더로, 타겟값을 특성의 범주별로 평균내어 그 값으로 인코딩
    TargetEncoder(min_samples_leaf=4,smoothing=4.0), 
    SimpleImputer(), 
    RandomForestClassifier(min_samples_leaf=4, n_jobs=-1, random_state=2)
)

dists = {
    
    'simpleimputer__strategy': ['mean', 'median'], 
    'randomforestclassifier__n_estimators': randint(10, 200), 
    'randomforestclassifier__max_depth': [5, 10, 15, 20, None], 
    'randomforestclassifier__max_features': uniform(0, 1) # max_features
}

model = RandomizedSearchCV(
    pipe, 
    param_distributions=dists, 
    n_iter=50, 
    cv=3, 
    scoring='neg_mean_absolute_error',  
    verbose=1,
    n_jobs=-1
)

model.fit(X_train,y_train)
with open('project/model.pkl','wb') as pickle_file:
    pickle.dump(model, pickle_file)

