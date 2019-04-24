import cx_Oracle as oc
from bs4 import BeautifulSoup
import requests

# get Boxoffice from Naver
url = 'https://search.naver.com/search.naver?sm=top_hty&fbm=1&ie=utf8&query=%EB%B0%95%EC%8A%A4%EC%98%A4%ED%94%BC%EC%8A%A4'
result = requests.get(url)
html = BeautifulSoup(result.content, 'html.parser')
div = html.findAll('strong', {'class': "scm_ellipsis_text"})

# get Boxoffice
boxoffice = []
for d in div:
    d = d.text
    boxoffice.append(d)

# get no, title from Boxoffice
for i in range(10):
    no = i + 1
    title = boxoffice[i]

    # Oracle Connection - insert
    conn = oc.connect('hyeminseo/hyeminseo@203.236.209.97:1521/XE')
    cursor = conn.cursor()
    cursor.execute('insert into boxoffice values(:no, :title)', no=int(no), title=str(title))
    conn.commit()
    cursor.close()
    conn.close