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
from pymongo import MongoClient

dbpath = 'project\culture.db'

conn = sqlite3.connect(dbpath)
cur = conn.cursor()
file = pd.read_sql("SELECT * FROM cultural;",conn, index_col=None)



HOST = 'culturerecommand.ly6sxbn.mongodb.net'
USER = 'user'
PASSWORD = '1121'
DATABASE_NAME = 'culture'
COLLECTION_NAME = 'recommand'
MONGO_URI = f"mongodb+srv://{USER}:{PASSWORD}@{HOST}/{DATABASE_NAME}?retryWrites=true&w=majority"

client = MongoClient(MONGO_URI)
collection =client[DATABASE_NAME][COLLECTION_NAME]

collection.insert_many(file.to_dict('records'))