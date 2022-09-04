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
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException,TimeoutException
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

options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ["enable-logging"])
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=options)
driver.implicitly_wait(100000)
driver.get('https://search.naver.com/search.naver?where=nexearch&sm=tab_etc&mra=bk00&qvt=0&query=%EC%B6%95%EC%A0%9C')
door_type='festibal'
#경남

driver.find_element(by=By.CSS_SELECTOR,value="#main_pack > div.sc_new.cs_common_module.case_list.color_1._cs_festival_list > div.cm_content_wrap > div > div > div.cm_tap_area.type_festival > div > div.type_scroll > ul > li:nth-child(1) > a > span.ico_check_wrap").click()
driver.implicitly_wait(100)
WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#main_pack > div.sc_new.cs_common_module.case_list.color_1._cs_festival_list > div.cm_content_wrap > div > div > div.cm_tap_area.type_festival > div > div.type_scroll > ul > li:nth-child(1) > a > span.ico_check_wrap"))).click()
driver.implicitly_wait(100)

WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.LINK_TEXT, "경남"))).click()
driver.implicitly_wait(100)

driver.find_element(by=By.LINK_TEXT,value="경남").click()
driver.implicitly_wait(100)
while True:
#mflick > div > div > div > div:nth-child(1) > div:nth-child(1)
    itemlist = driver.find_elements(By.CSS_SELECTOR,'#mflick > div > div > div')
    total_str = driver.find_element(By.CSS_SELECTOR,'#main_pack > div.sc_new.cs_common_module.case_list.color_1._cs_festival_list > div.cm_content_wrap > div > div > div.cm_tab_content > div.cm_paging_area > div > span > span._total').text
    total_num = int(total_str)
    for i in range(1, total_num):
        items = driver.find_elements(By.CSS_SELECTOR,f'#mflick > div > div > div > div:nth-child({i}) > div')
        for item in items:
            #mflick > div > div > div > div:nth-child(1) > div:nth-child(1) > div.data_area > div > div.title > div > strong > a
            title = item.find_element(By.CSS_SELECTOR,'div.data_area > div > div.title > div > strong > a').text
            #mflick > div > div > div > div:nth-child(1) > div:nth-child(1) > div.data_area > div > div.info > dl > dd:nth-child(2)
            period = item.find_element(By.CSS_SELECTOR,'div.data_area > div > div.info > dl > dd:nth-child(2)').text
            start_period,end_period = period.split('~')
            #mflick > div > div > div > div:nth-child(1) > div:nth-child(1) > div.data_area > div > div.info > dl > dd:nth-child(4)
            location = item.find_element(By.CSS_SELECTOR,'div.data_area > div > div.info > dl > dd:nth-child(4)').text
            #mflick > div > div > div > div:nth-child(1) > div:nth-child(1) > div.data_area > a > img
            poster = item.find_element(By.CSS_SELECTOR,'div.data_area > a > img').get_attribute('src')
            region = "타지역"
        #데이터베이스에 넣기    
            base_sql = """INSERT INTO outdoor(door_type,title, region, start_period, end_period, location, poster) values("{}","{}", '{}', '{}', '{}', '{}', '{}')"""
            sql_query = base_sql.format(door_type,title, region, start_period, end_period, location, poster)
            cur.execute(sql_query)
            conn.commit()
            time.sleep(4)
        try:
            WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.LINK_TEXT, "다음"))).click()
            time.sleep(4)
        except NoSuchElementException:
            break
    cur_page = driver.find_element(By.CSS_SELECTOR, '#main_pack > div.sc_new.cs_common_module.case_list.color_1._cs_festival_list > div.cm_content_wrap > div > div > div.cm_tab_content > div.cm_paging_area > div > span > strong').text
    
    driver.implicitly_wait(100)
    end_page = driver.find_element(By.CSS_SELECTOR, '#main_pack > div.sc_new.cs_common_module.case_list.color_1._cs_festival_list > div.cm_content_wrap > div > div > div.cm_tab_content > div.cm_paging_area > div > span > span._total').text
    driver.implicitly_wait(15)
    if(cur_page==end_page):
        break

driver.quit()
options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ["enable-logging"])
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=options)
driver.implicitly_wait(100000)
driver.get('https://search.naver.com/search.naver?where=nexearch&sm=tab_etc&mra=bk00&qvt=0&query=%EC%B6%95%EC%A0%9C')

#경북
driver.find_element(by=By.CSS_SELECTOR,value="#main_pack > div.sc_new.cs_common_module.case_list.color_1._cs_festival_list > div.cm_content_wrap > div > div > div.cm_tap_area.type_festival > div > div.type_scroll > ul > li:nth-child(1) > a > span.ico_check_wrap").click()
driver.implicitly_wait(100)
WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#main_pack > div.sc_new.cs_common_module.case_list.color_1._cs_festival_list > div.cm_content_wrap > div > div > div.cm_tap_area.type_festival > div > div.type_scroll > ul > li:nth-child(1) > a > span.ico_check_wrap"))).click()
driver.implicitly_wait(100)

WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.LINK_TEXT, "경북"))).click()
driver.implicitly_wait(100)

driver.find_element(by=By.LINK_TEXT,value="경북").click()
driver.implicitly_wait(100)

while True:
#mflick > div > div > div > div:nth-child(1) > div:nth-child(1)
    itemlist = driver.find_elements(By.CSS_SELECTOR,'#mflick > div > div > div')
    total_str = driver.find_element(By.CSS_SELECTOR,'#main_pack > div.sc_new.cs_common_module.case_list.color_1._cs_festival_list > div.cm_content_wrap > div > div > div.cm_tab_content > div.cm_paging_area > div > span > span._total').text
    total_num = int(total_str)
    for i in range(1, total_num):
        items = driver.find_elements(By.CSS_SELECTOR,f'#mflick > div > div > div > div:nth-child({i}) > div')
        for item in items:
            #mflick > div > div > div > div:nth-child(1) > div:nth-child(1) > div.data_area > div > div.title > div > strong > a
            title = item.find_element(By.CSS_SELECTOR,'div.data_area > div > div.title > div > strong > a').text
            #mflick > div > div > div > div:nth-child(1) > div:nth-child(1) > div.data_area > div > div.info > dl > dd:nth-child(2)
            period = item.find_element(By.CSS_SELECTOR,'div.data_area > div > div.info > dl > dd:nth-child(2)').text
            start_period,end_period = period.split('~')
            #mflick > div > div > div > div:nth-child(1) > div:nth-child(1) > div.data_area > div > div.info > dl > dd:nth-child(4)
            location = item.find_element(By.CSS_SELECTOR,'div.data_area > div > div.info > dl > dd:nth-child(4)').text
            #mflick > div > div > div > div:nth-child(1) > div:nth-child(1) > div.data_area > a > img
            poster = item.find_element(By.CSS_SELECTOR,'div.data_area > a > img').get_attribute('src')
            region = "타지역"
        #데이터베이스에 넣기    
            base_sql = """INSERT INTO outdoor(door_type,title, region, start_period, end_period, location, poster) values("{}","{}", '{}', '{}', '{}', '{}', '{}')"""
            sql_query = base_sql.format(door_type,title, region, start_period, end_period, location, poster)
            cur.execute(sql_query)
            conn.commit()
            time.sleep(4)
        try:
            WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.LINK_TEXT, "다음"))).click()
            time.sleep(4)
        except NoSuchElementException:
            break
    cur_page = driver.find_element(By.CSS_SELECTOR, '#main_pack > div.sc_new.cs_common_module.case_list.color_1._cs_festival_list > div.cm_content_wrap > div > div > div.cm_tab_content > div.cm_paging_area > div > span > strong').text
    
    driver.implicitly_wait(100)
    end_page = driver.find_element(By.CSS_SELECTOR, '#main_pack > div.sc_new.cs_common_module.case_list.color_1._cs_festival_list > div.cm_content_wrap > div > div > div.cm_tab_content > div.cm_paging_area > div > span > span._total').text
    driver.implicitly_wait(15)

    if(cur_page==end_page):
        break

driver.quit()

options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ["enable-logging"])
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=options)
driver.implicitly_wait(100000)
driver.get('https://search.naver.com/search.naver?where=nexearch&sm=tab_etc&mra=bk00&qvt=0&query=%EC%B6%95%EC%A0%9C')

#전북
driver.find_element(by=By.CSS_SELECTOR,value="#main_pack > div.sc_new.cs_common_module.case_list.color_1._cs_festival_list > div.cm_content_wrap > div > div > div.cm_tap_area.type_festival > div > div.type_scroll > ul > li:nth-child(1) > a > span.ico_check_wrap").click()
driver.implicitly_wait(100)
WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#main_pack > div.sc_new.cs_common_module.case_list.color_1._cs_festival_list > div.cm_content_wrap > div > div > div.cm_tap_area.type_festival > div > div.type_scroll > ul > li:nth-child(1) > a > span.ico_check_wrap"))).click()
driver.implicitly_wait(100)

WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.LINK_TEXT, "전북"))).click()
driver.implicitly_wait(100)

driver.find_element(by=By.LINK_TEXT,value="전북").click()
driver.implicitly_wait(100)

while True:
#mflick > div > div > div > div:nth-child(1) > div:nth-child(1)
    itemlist = driver.find_elements(By.CSS_SELECTOR,'#mflick > div > div > div')
    total_str = driver.find_element(By.CSS_SELECTOR,'#main_pack > div.sc_new.cs_common_module.case_list.color_1._cs_festival_list > div.cm_content_wrap > div > div > div.cm_tab_content > div.cm_paging_area > div > span > span._total').text
    total_num = int(total_str)
    for i in range(1, total_num):
        items = driver.find_elements(By.CSS_SELECTOR,f'#mflick > div > div > div > div:nth-child({i}) > div')
        for item in items:
            #mflick > div > div > div > div:nth-child(1) > div:nth-child(1) > div.data_area > div > div.title > div > strong > a
            title = item.find_element(By.CSS_SELECTOR,'div.data_area > div > div.title > div > strong > a').text
            #mflick > div > div > div > div:nth-child(1) > div:nth-child(1) > div.data_area > div > div.info > dl > dd:nth-child(2)
            period = item.find_element(By.CSS_SELECTOR,'div.data_area > div > div.info > dl > dd:nth-child(2)').text
            start_period,end_period = period.split('~')
            #mflick > div > div > div > div:nth-child(1) > div:nth-child(1) > div.data_area > div > div.info > dl > dd:nth-child(4)
            location = item.find_element(By.CSS_SELECTOR,'div.data_area > div > div.info > dl > dd:nth-child(4)').text
            #mflick > div > div > div > div:nth-child(1) > div:nth-child(1) > div.data_area > a > img
            poster = item.find_element(By.CSS_SELECTOR,'div.data_area > a > img').get_attribute('src')
            region = "타지역"
        #데이터베이스에 넣기    
            try:
                base_sql = """INSERT INTO outdoor(door_type,title, region, start_period, end_period, location, poster) values("{}","{}", '{}', '{}', '{}', '{}', '{}')"""
            finally:
                continue
            sql_query = base_sql.format(door_type,title, region, start_period, end_period, location, poster)
            cur.execute(sql_query)
            conn.commit()
            time.sleep(4)
        try:
            WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.LINK_TEXT, "다음"))).click()
            time.sleep(4)
        except:
            break
    cur_page = driver.find_element(By.CSS_SELECTOR, '#main_pack > div.sc_new.cs_common_module.case_list.color_1._cs_festival_list > div.cm_content_wrap > div > div > div.cm_tab_content > div.cm_paging_area > div > span > strong').text
    
    driver.implicitly_wait(100)
    end_page = driver.find_element(By.CSS_SELECTOR, '#main_pack > div.sc_new.cs_common_module.case_list.color_1._cs_festival_list > div.cm_content_wrap > div > div > div.cm_tab_content > div.cm_paging_area > div > span > span._total').text
    driver.implicitly_wait(15)
    if(cur_page==end_page):
        break


# driver.quit()
options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ["enable-logging"])
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=options)
driver.implicitly_wait(100000)
driver.get('https://search.naver.com/search.naver?where=nexearch&sm=tab_etc&mra=bk00&qvt=0&query=%EC%B6%95%EC%A0%9C')

#강원
driver.find_element(by=By.CSS_SELECTOR,value="#main_pack > div.sc_new.cs_common_module.case_list.color_1._cs_festival_list > div.cm_content_wrap > div > div > div.cm_tap_area.type_festival > div > div.type_scroll > ul > li:nth-child(1) > a > span.ico_check_wrap").click()
driver.implicitly_wait(100)
WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#main_pack > div.sc_new.cs_common_module.case_list.color_1._cs_festival_list > div.cm_content_wrap > div > div > div.cm_tap_area.type_festival > div > div.type_scroll > ul > li:nth-child(1) > a > span.ico_check_wrap"))).click()
driver.implicitly_wait(100)

WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.LINK_TEXT, "강원"))).click()
driver.implicitly_wait(100)

driver.find_element(by=By.LINK_TEXT,value="강원").click()
driver.implicitly_wait(100)

while True:
#mflick > div > div > div > div:nth-child(1) > div:nth-child(1)
    itemlist = driver.find_elements(By.CSS_SELECTOR,'#mflick > div > div > div')
    total_str = driver.find_element(By.CSS_SELECTOR,'#main_pack > div.sc_new.cs_common_module.case_list.color_1._cs_festival_list > div.cm_content_wrap > div > div > div.cm_tab_content > div.cm_paging_area > div > span > span._total').text
    total_num = int(total_str)
    for i in range(1, total_num):
        items = driver.find_elements(By.CSS_SELECTOR,f'#mflick > div > div > div > div:nth-child({i}) > div')
        for item in items:
            #mflick > div > div > div > div:nth-child(1) > div:nth-child(1) > div.data_area > div > div.title > div > strong > a
            title = item.find_element(By.CSS_SELECTOR,'div.data_area > div > div.title > div > strong > a').text
            #mflick > div > div > div > div:nth-child(1) > div:nth-child(1) > div.data_area > div > div.info > dl > dd:nth-child(2)
            period = item.find_element(By.CSS_SELECTOR,'div.data_area > div > div.info > dl > dd:nth-child(2)').text
            start_period,end_period = period.split('~')
            #mflick > div > div > div > div:nth-child(1) > div:nth-child(1) > div.data_area > div > div.info > dl > dd:nth-child(4)
            location = item.find_element(By.CSS_SELECTOR,'div.data_area > div > div.info > dl > dd:nth-child(4)').text
            #mflick > div > div > div > div:nth-child(1) > div:nth-child(1) > div.data_area > a > img
            poster = item.find_element(By.CSS_SELECTOR,'div.data_area > a > img').get_attribute('src')
            region = "타지역"
        #데이터베이스에 넣기    
            base_sql = """INSERT INTO outdoor(door_type,title, region, start_period, end_period, location, poster) values("{}","{}", '{}', '{}', '{}', '{}', '{}')"""
            sql_query = base_sql.format(door_type,title, region, start_period, end_period, location, poster)
            cur.execute(sql_query)
            conn.commit()
            time.sleep(4)
        try:
            WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.LINK_TEXT, "다음"))).click()
            time.sleep(4)
        except:
            break
    cur_page = driver.find_element(By.CSS_SELECTOR, '#main_pack > div.sc_new.cs_common_module.case_list.color_1._cs_festival_list > div.cm_content_wrap > div > div > div.cm_tab_content > div.cm_paging_area > div > span > strong').text
    
    driver.implicitly_wait(100)
    end_page = driver.find_element(By.CSS_SELECTOR, '#main_pack > div.sc_new.cs_common_module.case_list.color_1._cs_festival_list > div.cm_content_wrap > div > div > div.cm_tab_content > div.cm_paging_area > div > span > span._total').text
    driver.implicitly_wait(15)
    if(cur_page==end_page):
        break

driver.quit()
options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ["enable-logging"])
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=options)
driver.implicitly_wait(100000)
driver.get('https://search.naver.com/search.naver?where=nexearch&sm=tab_etc&mra=bk00&qvt=0&query=%EC%B6%95%EC%A0%9C')

#제주
driver.find_element(by=By.CSS_SELECTOR,value="#main_pack > div.sc_new.cs_common_module.case_list.color_1._cs_festival_list > div.cm_content_wrap > div > div > div.cm_tap_area.type_festival > div > div.type_scroll > ul > li:nth-child(1) > a > span.ico_check_wrap").click()
driver.implicitly_wait(100)
WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#main_pack > div.sc_new.cs_common_module.case_list.color_1._cs_festival_list > div.cm_content_wrap > div > div > div.cm_tap_area.type_festival > div > div.type_scroll > ul > li:nth-child(1) > a > span.ico_check_wrap"))).click()
driver.implicitly_wait(100)

WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.LINK_TEXT, "제주"))).click()
driver.implicitly_wait(100)

driver.find_element(by=By.LINK_TEXT,value="제주").click()
driver.implicitly_wait(100)

while True:
#mflick > div > div > div > div:nth-child(1) > div:nth-child(1)
    itemlist = driver.find_elements(By.CSS_SELECTOR,'#mflick > div > div > div')
    total_str = driver.find_element(By.CSS_SELECTOR,'#main_pack > div.sc_new.cs_common_module.case_list.color_1._cs_festival_list > div.cm_content_wrap > div > div > div.cm_tab_content > div.cm_paging_area > div > span > span._total').text
    total_num = int(total_str)
    for i in range(1, total_num):
        items = driver.find_elements(By.CSS_SELECTOR,f'#mflick > div > div > div > div:nth-child({i}) > div')
        for item in items:
            #mflick > div > div > div > div:nth-child(1) > div:nth-child(1) > div.data_area > div > div.title > div > strong > a
            title = item.find_element(By.CSS_SELECTOR,'div.data_area > div > div.title > div > strong > a').text
            #mflick > div > div > div > div:nth-child(1) > div:nth-child(1) > div.data_area > div > div.info > dl > dd:nth-child(2)
            period = item.find_element(By.CSS_SELECTOR,'div.data_area > div > div.info > dl > dd:nth-child(2)').text
            start_period,end_period = period.split('~')
            #mflick > div > div > div > div:nth-child(1) > div:nth-child(1) > div.data_area > div > div.info > dl > dd:nth-child(4)
            location = item.find_element(By.CSS_SELECTOR,'div.data_area > div > div.info > dl > dd:nth-child(4)').text
            #mflick > div > div > div > div:nth-child(1) > div:nth-child(1) > div.data_area > a > img
            poster = item.find_element(By.CSS_SELECTOR,'div.data_area > a > img').get_attribute('src')
            region = "타지역"
        #데이터베이스에 넣기    
            base_sql = """INSERT INTO outdoor(door_type,title, region, start_period, end_period, location, poster) values("{}","{}", '{}', '{}', '{}', '{}', '{}')"""
            sql_query = base_sql.format(door_type,title, region, start_period, end_period, location, poster)
            cur.execute(sql_query)
            conn.commit()
            time.sleep(4)
        try:
            WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.LINK_TEXT, "다음"))).click()
            time.sleep(4)
        except:
            break
    cur_page = driver.find_element(By.CSS_SELECTOR, '#main_pack > div.sc_new.cs_common_module.case_list.color_1._cs_festival_list > div.cm_content_wrap > div > div > div.cm_tab_content > div.cm_paging_area > div > span > strong').text
    
    driver.implicitly_wait(100)
    end_page = driver.find_element(By.CSS_SELECTOR, '#main_pack > div.sc_new.cs_common_module.case_list.color_1._cs_festival_list > div.cm_content_wrap > div > div > div.cm_tab_content > div.cm_paging_area > div > span > span._total').text
    driver.implicitly_wait(15)

    if(cur_page==end_page):
        break
driver.quit()


options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ["enable-logging"])
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=options)
driver.implicitly_wait(100000)
driver.get('https://search.naver.com/search.naver?where=nexearch&sm=tab_etc&mra=bk00&qvt=0&query=%EC%B6%95%EC%A0%9C')

#전남
driver.find_element(by=By.CSS_SELECTOR,value="#main_pack > div.sc_new.cs_common_module.case_list.color_1._cs_festival_list > div.cm_content_wrap > div > div > div.cm_tap_area.type_festival > div > div.type_scroll > ul > li:nth-child(1) > a > span.ico_check_wrap").click()
driver.implicitly_wait(100)
WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#main_pack > div.sc_new.cs_common_module.case_list.color_1._cs_festival_list > div.cm_content_wrap > div > div > div.cm_tap_area.type_festival > div > div.type_scroll > ul > li:nth-child(1) > a > span.ico_check_wrap"))).click()
driver.implicitly_wait(100)

WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.LINK_TEXT, "전남"))).click()
driver.implicitly_wait(100)

driver.find_element(by=By.LINK_TEXT,value="전남").click()
driver.implicitly_wait(100)

while True:
#mflick > div > div > div > div:nth-child(1) > div:nth-child(1)
    itemlist = driver.find_elements(By.CSS_SELECTOR,'#mflick > div > div > div')
    total_str = driver.find_element(By.CSS_SELECTOR,'#main_pack > div.sc_new.cs_common_module.case_list.color_1._cs_festival_list > div.cm_content_wrap > div > div > div.cm_tab_content > div.cm_paging_area > div > span > span._total').text
    total_num = int(total_str)
    for i in range(1, total_num):
        items = driver.find_elements(By.CSS_SELECTOR,f'#mflick > div > div > div > div:nth-child({i}) > div')
        for item in items:
            #mflick > div > div > div > div:nth-child(1) > div:nth-child(1) > div.data_area > div > div.title > div > strong > a
            title = item.find_element(By.CSS_SELECTOR,'div.data_area > div > div.title > div > strong > a').text
            #mflick > div > div > div > div:nth-child(1) > div:nth-child(1) > div.data_area > div > div.info > dl > dd:nth-child(2)
            period = item.find_element(By.CSS_SELECTOR,'div.data_area > div > div.info > dl > dd:nth-child(2)').text
            start_period,end_period = period.split('~')
            #mflick > div > div > div > div:nth-child(1) > div:nth-child(1) > div.data_area > div > div.info > dl > dd:nth-child(4)
            location = item.find_element(By.CSS_SELECTOR,'div.data_area > div > div.info > dl > dd:nth-child(4)').text
            #mflick > div > div > div > div:nth-child(1) > div:nth-child(1) > div.data_area > a > img
            poster = item.find_element(By.CSS_SELECTOR,'div.data_area > a > img').get_attribute('src')
            region = "타지역"
        #데이터베이스에 넣기
            try:    
                base_sql = """INSERT INTO outdoor(door_type,title, region, start_period, end_period, location, poster) values("{}","{}", '{}', '{}', '{}', '{}', '{}')"""
            finally:
                base_sql = """INSERT INTO outdoor(door_type,title, region, start_period, end_period, location, poster) values("{}",'{}', '{}', '{}', '{}', '{}', '{}')"""

            sql_query = base_sql.format(door_type,title, region, start_period, end_period, location, poster)
            cur.execute(sql_query)
            conn.commit()
            time.sleep(4)
        try:
            WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.LINK_TEXT, "다음"))).click()
            time.sleep(4)
        except NoSuchElementException:
            break
    cur_page = driver.find_element(By.CSS_SELECTOR, '#main_pack > div.sc_new.cs_common_module.case_list.color_1._cs_festival_list > div.cm_content_wrap > div > div > div.cm_tab_content > div.cm_paging_area > div > span > strong').text
    
    driver.implicitly_wait(100)
    end_page = driver.find_element(By.CSS_SELECTOR, '#main_pack > div.sc_new.cs_common_module.case_list.color_1._cs_festival_list > div.cm_content_wrap > div > div > div.cm_tab_content > div.cm_paging_area > div > span > span._total').text
    driver.implicitly_wait(15)
    if(cur_page==end_page):
        break

driver.quit()