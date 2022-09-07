#__init__.py
from this import s
import pandas as pd
import sqlite3
from flask import Flask, render_template, redirect, url_for
from bs4 import BeautifulSoup
from flask import Blueprint, request
import pickle
import re
app = Flask(__name__)
dbpath = 'project\culture.db'

@app.route('/',methods =['GET','POST'])
def startpage():
    #해당 축제 선택'
    conn = sqlite3.connect(r'C:\\Users\\InKoo\\Section3\\Cultural-Recommand\\project\\culture.db')
    cur = conn.cursor()
    train = pd.read_sql("SELECT * FROM traindata;",conn, index_col=None)
    train = train.drop(columns=['level_0'])
    if request.method == 'POST':
        title = request.form['title_name']
        select_title=title
        select_cond = train['title']==title
        select_data = train[select_cond]
        if(select_data.empty):
            return redirect(url_for('errorpage'))
        model=None
        with open(r'C:\Users\InKoo\Section3\Cultural-Recommand\project\model.pkl', 'rb') as pickle_file:
            model=pickle.load(pickle_file)
        pred = model.predict(select_data)
        return redirect(url_for('selectdata', region_number=pred))

    return render_template('main.html')

@app.route('/select/<region_number>',methods =['GET','POST'])
def selectdata(region_number):
    conn = sqlite3.connect(r'C:\Users\InKoo\Section3\Cultural-Recommand\project\culture.db')
    cur = conn.cursor()
    culture = pd.read_sql("SELECT * FROM cultural;",conn, index_col=None)
    rnstr = re.sub(r'[^0-9]', '', region_number)
    door1 = int(rnstr)
    cult3= culture[culture['region_number']==door1]
    cult4 = cult3
    return render_template('select.html',cult4=cult4)

@app.route('/errorpage')
def errorpage():

    return render_template('errorpage.html')

if __name__ == "__main__":
    app.run(debug=True)



