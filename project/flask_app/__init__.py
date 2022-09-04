#__init__.py
from this import s
import pandas as pd
import sqlite3
from flask import Flask, render_template, redirect, url_for
from bs4 import BeautifulSoup
from flask import Blueprint, request
import pickle

dbpath = 'project\exfes.db'

conn = sqlite3.connect(dbpath)
cur = conn.cursor()

culture = pd.read_sql("SELECT * FROM outdoor;",conn, index_col=None)

select_title = ""

@app.route('/',methods =['GET','POST'])
def startpage():
    #해당 축제 선택
    cultur2 =culture.copy()
    cultur2.drop(columns=['end_period','start_period','door'])
    if request.method == 'POST':
        title = request.form['title_name']
        select_title=title
        select_cond = cultur2['title']==title
        select_data = cultur2[select_cond]
        model=None
        with open('project/model.pkl', 'rb') as pickle_file:
            model=pickle.load(pickle_file)
        pred = model.predict(select_data)
        return redirect(url_for(selectdata, door=pred))

    return render_template('project\flask_app\main.html')

@app.route('/select')
def selectdata(door):
    content_title = request.form['title_name']
    door1 = door
    cult3= culture[culture['door']==door1]
    cult4 = cult3.head()
    return render_template('project\flask_app\select.html',cult4)


