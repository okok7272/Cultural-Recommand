import pandas as pd
import numpy as np
import pickle
import sqlite3
import pymysql
from sqlalchemy import create_engine
from datetime import datetime

# HOST = 'cluster0.xcojk3n.mongodb.net'
# USER = 'whaleuser'
# PASSWORD = 'whale1234'
# DATABASE_NAME = 'myFirstDatabase'
# COLLECTION_NAME = 'octokit_repos'
# MONGO_URI = f"mongodb+srv://{USER}:{PASSWORD}@{HOST}/{DATABASE_NAME}?retryWrites=true&w=majority"

# client = MongoClient(MONGO_URI)
# collection =client[DATABASE_NAME][COLLECTION_NAME]
# names = {}

dbpath = 'project\exfes.db'

conn = sqlite3.connect(dbpath)
cur = conn.cursor()

culture = pd.read_sql("SELECT * FROM outdoor;",conn, index_col=None)

def errorcode( x):
  if(x == "오픈런"):
    x="2024.12.31."
  return x
culture['end_period']= culture['end_period'].apply(errorcode)
culture['end_period']= culture['end_period'].str.rstrip('.')
culture['start_period']=culture['start_period'].str.rstrip('.')

culture[['syear','smonth','sday']]= culture['start_period'].str.split('.',expand=True)
culture[['eyear','emonth','eday']]= culture['end_period'].str.split('.',expand=True)
culture[['syear','smonth','sday']]= culture[['syear','smonth','sday']].apply(pd.to_numeric)
culture[['eyear','emonth','eday']]= culture[['eyear','emonth','eday']].apply(pd.to_numeric)

culture['end_period']= culture['end_period'].replace('.','')
culture['start_period']=culture['start_period'].replace('.','')
culture['end_period']=pd.to_datetime(culture['end_period'])
culture['start_period']=pd.to_datetime(culture['start_period'])

def typeEnc(x):
    if x =='festibal':
        x=1
    else:
        x=2
    return x

culture['door']= culture['door_type'].apply(typeEnc)

sqlcon = sqlite3.connect('project/culture.db')
culture.to_sql('outdoor',sqlcon)