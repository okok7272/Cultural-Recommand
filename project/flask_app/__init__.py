#__init__.py
from this import s
import pandas as pd
import sqlite3
from flask import Flask, render_template, redirect, url_for
from bs4 import BeautifulSoup
from flask import Blueprint, request
import pickle

app = Flask(__name__)
dbpath = 'project\culture.db'



@app.route('/',methods =['GET','POST'])
def startpage():
    #해당 축제 선택'
    conn = sqlite3.connect(r'C:\\Users\\InKoo\\Section3\\Cultural-Recommand\\project\\culture.db')
    cur = conn.cursor()
    culture = pd.read_sql("SELECT * FROM cultural;",conn, index_col=None)

    cultur2 =culture.copy()
    cultur2.drop(columns=['end_period','start_period','door','region_number'])
    if request.method == 'POST':
        title = request.form['title_name']
        select_title=title
        select_cond = cultur2['title']==title
        select_data = cultur2[select_cond]
        if(select_data.empty):
            return redirect(url_for('/errorpage'))
        model=None
        with open(r'C:\Users\InKoo\Section3\Cultural-Recommand\project\model.pkl', 'rb') as pickle_file:
            model=pickle.load(pickle_file)
        pred = model.predict(select_data)
        return redirect(url_for('selectdata', door=pred))

    return render_template('main.html')

@app.route('/select',methods =['GET','POST'])
def selectdata(door):
    conn = sqlite3.connect(r'C:\Users\InKoo\Section3\Cultural-Recommand\project\culture.db')
    cur = conn.cursor()
    culture = pd.read_sql("SELECT * FROM cultural;",conn, index_col=None)

    content_title = request.form['title_name']
    door1 = door
    cult3= culture[culture['region_number']==door1]
    cult3.to_json('project/cult.json',orient='records')
    cult4 = cult3
    return render_template('select.html',cult4)

@app.route('/errorpage')
def errorpage():

    return render_template('errorpage.html')

if __name__ == "__main__":
    app.run(debug=True)



