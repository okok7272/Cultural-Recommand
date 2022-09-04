#__init__.py
import pandas as pd
import sqlite3
from flask import Flask, render_template
from bs4 import BeautifulSoup
from flask import Blueprint, request

dbpath = 'project\exfes.db'

conn = sqlite3.connect(dbpath)
cur = conn.cursor()

culture = pd.read_sql("SELECT * FROM outdoor;",conn, index_col=None)
def create_app(config=None):
    app = Flask(__name__)
    if config is not None:
        app.config.update(config)
    from flask_app.views.main_view import main_bp
    from flask_app.views.user_view import user_bp
    
    app.register_blueprint(main_bp)
    app.register_blueprint(user_bp, url_prefix='/api')

    @app.route('/')
    def startpage():
    #해당 축제 선택
        culture =culture

        return render_template('project\flask_app\main.html')

    @app.route('/select')
    def MonthrecommandPage():
        content_title = request.form()
        
        return 0

    return app


