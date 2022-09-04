import pandas as pd
import requests
import re
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
import csv
import sqlite3
import glob
import os
from PIL import Image

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys

#database 구축
dbpath = "exfes.db"
conn = sqlite3.connect(dbpath)
cur = conn.cursor()

script = """ 
DROP TABLE IF EXISTS outdoor;

CREATE TABLE outdoor(
  id INTEGER PRIMARY KEY AUTOINCREMENT,  
  door_type TEXT,
  title TEXT,
  region    TEXT,                             
  start_period  TEXT,
  end_period    TEXT,
  location  TEXT,                         
  poster    TEXT    
);
"""

cur.executescript(script)
door_type = 'exhibit'
#분류, title, 사진,기간(시작, 종료), 장소, 주소
options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ["enable-logging"])
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=options)
driver.implicitly_wait(100000)


driver.get('https://search.naver.com/search.naver?where=nexearch&sm=top_sly.hst&fbm=1&acr=2&ie=utf8&query=%EC%A0%84%EC%8B%9C%ED%9A%8C')
#서울
WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.LINK_TEXT, "서울"))).click()
driver.find_element(by=By.LINK_TEXT,value="서울").click()
driver.implicitly_wait(100)
time.sleep(2)
while True:
    #mflick > div > div > div > div
    items = driver.find_elements(By.CSS_SELECTOR,'#mflick > div > div > div > div > div')
    driver.implicitly_wait(100)

    for item in items:
    # div.data_area > div > div.title > div > strong > a
    ##mflick > div > div > div > div > div:nth-child(1) > div.data_area > div > div.title > div > strong > a
        title = item.find_element(By.CSS_SELECTOR,'div.data_area > div > div.title > div > strong > a').text
    ##mflick > div > div > div > div > div:nth-child(1) > div.data_area > div > div.info > dl:nth-child(1) > dd
        period = item.find_element(By.CSS_SELECTOR,'div.data_area > div > div.info > dl:nth-child(1) > dd').text
        start_period,end_period = period.split('~')
    ##mflick > div > div > div > div > div:nth-child(1) > div.data_area > div > div.info > dl:nth-child(2) > dd > a
        location = item.find_element(By.CSS_SELECTOR,'div.data_area > div > div.info > dl:nth-child(2) > dd > a').text
    ##mflick > div > div > div > div > div:nth-child(2) > div.data_area > a > img
        poster = item.find_element(By.CSS_SELECTOR,'div.data_area > a > img').get_attribute('src')
        region = "서울"
        #데이터베이스에 넣기    
        base_sql = """INSERT INTO outdoor(door_type,title, region, start_period, end_period, location, poster) values("{}","{}", '{}', '{}', '{}', '{}', '{}')"""
        sql_query = base_sql.format(door_type,title, region, start_period, end_period, location, poster)
        cur.execute(sql_query)
        conn.commit()
        print(title ,period, location)
    time.sleep(4)

    WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.LINK_TEXT, "다음"))).click()
    time.sleep(4)
    cur_page = driver.find_element(By.CSS_SELECTOR,'#main_pack > div.sc_new.cs_common_module.case_list.color_1._kgs_art_exhibition > div.cm_content_wrap > div > div > div.cm_paging_area._page > div > span > strong').text
    driver.implicitly_wait(100)
    end_page = driver.find_element(By.CSS_SELECTOR,'#main_pack > div.sc_new.cs_common_module.case_list.color_1._kgs_art_exhibition > div.cm_content_wrap > div > div > div.cm_paging_area._page > div > span > span._total').text
    if(cur_page==end_page):
        break

#경기
WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.LINK_TEXT, "경기"))).click()
driver.find_element(by=By.LINK_TEXT,value="경기").click()
driver.implicitly_wait(100)
time.sleep(2)
while True:
    items = driver.find_elements(By.CSS_SELECTOR,'#mflick > div > div > div > div > div')
    driver.implicitly_wait(100)

    for item in items:
    # div.data_area > div > div.title > div > strong > a
    ##mflick > div > div > div > div > div:nth-child(1) > div.data_area > div > div.title > div > strong > a
        title = item.find_element(By.CSS_SELECTOR,'div.data_area > div > div.title > div > strong > a').text
    ##mflick > div > div > div > div > div:nth-child(1) > div.data_area > div > div.info > dl:nth-child(1) > dd
        period = item.find_element(By.CSS_SELECTOR,'div.data_area > div > div.info > dl:nth-child(1) > dd').text
        start_period,end_period = period.split('~')
    ##mflick > div > div > div > div > div:nth-child(1) > div.data_area > div > div.info > dl:nth-child(2) > dd > a
        location = item.find_element(By.CSS_SELECTOR,'div.data_area > div > div.info > dl:nth-child(2) > dd > a').text
    ##mflick > div > div > div > div > div:nth-child(2) > div.data_area > a > img
        poster = item.find_element(By.CSS_SELECTOR,'div.data_area > a > img').get_attribute('src')
        region = "경기"
        #데이터베이스에 넣기    
        base_sql = """INSERT INTO outdoor(door_type,title, region, start_period, end_period, location, poster) values("{}","{}", '{}', '{}', '{}', "{}", '{}')"""
        sql_query = base_sql.format(door_type,title, region, start_period, end_period, location, poster)
        cur.execute(sql_query)
        conn.commit()
        print(title ,period, location)
    time.sleep(5)
    driver.implicitly_wait(100)
    WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.LINK_TEXT, "다음"))).click()
    time.sleep(4)
    cur_page = driver.find_element(By.CSS_SELECTOR,'#main_pack > div.sc_new.cs_common_module.case_list.color_1._kgs_art_exhibition > div.cm_content_wrap > div > div > div.cm_paging_area._page > div > span > strong').text
    end_page = driver.find_element(By.CSS_SELECTOR,'#main_pack > div.sc_new.cs_common_module.case_list.color_1._kgs_art_exhibition > div.cm_content_wrap > div > div > div.cm_paging_area._page > div > span > span._total').text
    if(cur_page==end_page):
        break

#부산
WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.LINK_TEXT, "부산"))).click()
driver.find_element(by=By.LINK_TEXT,value="부산").click()
driver.implicitly_wait(100)
time.sleep(2)
while True:
    items = driver.find_elements(By.CSS_SELECTOR,'#mflick > div > div > div > div > div')
    driver.implicitly_wait(100)

    for item in items:
    # div.data_area > div > div.title > div > strong > a
    ##mflick > div > div > div > div > div:nth-child(1) > div.data_area > div > div.title > div > strong > a
        title = item.find_element(By.CSS_SELECTOR,'div.data_area > div > div.title > div > strong > a').text
    ##mflick > div > div > div > div > div:nth-child(1) > div.data_area > div > div.info > dl:nth-child(1) > dd
        period = item.find_element(By.CSS_SELECTOR,'div.data_area > div > div.info > dl:nth-child(1) > dd').text
        start_period,end_period = period.split('~')
    ##mflick > div > div > div > div > div:nth-child(1) > div.data_area > div > div.info > dl:nth-child(2) > dd > a
        location = item.find_element(By.CSS_SELECTOR,'div.data_area > div > div.info > dl:nth-child(2) > dd > a').text
    ##mflick > div > div > div > div > div:nth-child(2) > div.data_area > a > img
        poster = item.find_element(By.CSS_SELECTOR,'div.data_area > a > img').get_attribute('src')
        region = "부산"
        driver.implicitly_wait(100)
        #데이터베이스에 넣기    
        base_sql = """INSERT INTO outdoor(door_type,title, region, start_period, end_period, location, poster) values("{}","{}", '{}', '{}', '{}', "{}", '{}')"""
        sql_query = base_sql.format(door_type,title, region, start_period, end_period, location, poster)
        cur.execute(sql_query)
        conn.commit()
        driver.implicitly_wait(100)
        print(title ,period, location)
    time.sleep(4)

    WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.LINK_TEXT, "다음"))).click()
    time.sleep(4)
    cur_page = driver.find_element(By.CSS_SELECTOR,'#main_pack > div.sc_new.cs_common_module.case_list.color_1._kgs_art_exhibition > div.cm_content_wrap > div > div > div.cm_paging_area._page > div > span > strong').text
    end_page = driver.find_element(By.CSS_SELECTOR,'#main_pack > div.sc_new.cs_common_module.case_list.color_1._kgs_art_exhibition > div.cm_content_wrap > div > div > div.cm_paging_area._page > div > span > span._total').text
    if(cur_page==end_page):
        break

#타지역
WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.LINK_TEXT, "타지역"))).click()
driver.find_element(by=By.LINK_TEXT,value="타지역").click()
driver.implicitly_wait(100)
time.sleep(2)
while True:
    items = driver.find_elements(By.CSS_SELECTOR,'#mflick > div > div > div > div > div')
    driver.implicitly_wait(100)

    for item in items:
    # div.data_area > div > div.title > div > strong > a
    ##mflick > div > div > div > div > div:nth-child(1) > div.data_area > div > div.title > div > strong > a
        title = item.find_element(By.CSS_SELECTOR,'div.data_area > div > div.title > div > strong > a').text
    ##mflick > div > div > div > div > div:nth-child(1) > div.data_area > div > div.info > dl:nth-child(1) > dd
        period = item.find_element(By.CSS_SELECTOR,'div.data_area > div > div.info > dl:nth-child(1) > dd').text
        start_period,end_period = period.split('~')
    ##mflick > div > div > div > div > div:nth-child(1) > div.data_area > div > div.info > dl:nth-child(2) > dd > a
        location = item.find_element(By.CSS_SELECTOR,'div.data_area > div > div.info > dl:nth-child(2) > dd > a').text
    ##mflick > div > div > div > div > div:nth-child(2) > div.data_area > a > img
        poster = item.find_element(By.CSS_SELECTOR,'div.data_area > a > img').get_attribute('src')
        driver.implicitly_wait(100)
        region = "타지역"
        #데이터베이스에 넣기    
        base_sql = """INSERT INTO outdoor(door_type,title, region, start_period, end_period, location, poster) values("{}","{}", '{}', '{}', '{}', "{}", '{}')"""
        sql_query = base_sql.format(door_type,title, region, start_period, end_period, location, poster)
        cur.execute(sql_query)
        conn.commit()
        print(title ,period, location)
    time.sleep(4)
    WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.LINK_TEXT, "다음"))).click()
    time.sleep(4)
    cur_page = driver.find_element(By.CSS_SELECTOR,'#main_pack > div.sc_new.cs_common_module.case_list.color_1._kgs_art_exhibition > div.cm_content_wrap > div > div > div.cm_paging_area._page > div > span > strong').text
    driver.implicitly_wait(100)
    end_page = driver.find_element(By.CSS_SELECTOR,'#main_pack > div.sc_new.cs_common_module.case_list.color_1._kgs_art_exhibition > div.cm_content_wrap > div > div > div.cm_paging_area._page > div > span > span._total').text
    if(cur_page==end_page):
        break
