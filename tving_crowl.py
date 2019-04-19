from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import cx_Oracle as oc
import os
import pandas as pd
import time
import re

driver = webdriver.Chrome()
driver.get("http://www.tving.com/movie/allm")
time.sleep(1)

body = driver.find_element_by_tag_name("body")
num_of_padedown = 5
while num_of_padedown:
    body.send_keys(Keys.PAGE_DOWN)
    time.sleep(0.2)
    num_of_padedown -= 1

html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')
li = soup.findAll('li')
for item in li:
    print(item)


# # Oracle Connection
# os.environ["NLS_LANG"] = ".AL32UTF8"
# START_VALUE = u"시작값입니다".encode('cp949')
# END_VALUE = u"종료값입니다".encode('cp949')
#
# conn = oc.connect('hyeminseo/hyeminseo@203.236.209.97:1521/XE')
# cursor = conn.cursor()
# cursor.execute('select * from member')
# print(cursor.fetchall())
#
# cursor.close()
# conn.close