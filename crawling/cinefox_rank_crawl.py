import cx_Oracle as oc
from bs4 import BeautifulSoup
import requests

# get Boxoffice from Naver
url = 'https://search.naver.com/search.naver?sm=top_hty&fbm=1&ie=utf8&query=%EB%B0%95%EC%8A%A4%EC%98%A4%ED%94%BC%EC%8A%A4'
result = requests.get(url)
html = BeautifulSoup(result.content, 'html.parser')
btn_area = html.findAll('a', {'class': "btn btn_reserve"})

# get rank, movie_no from Boxoffice
for i in range(10):
    rank = i + 1

    href = btn_area[i]['href']
    split = href.split('=')[1]
    movie_no = split.split('&')[0]

    # Oracle Connection - insert
    conn = oc.connect('hyeminseo/hyeminseo@203.236.209.97:1521/XE')
    cursor = conn.cursor()
    stmt = 'UPDATE movie SET movie_nowrank = :r WHERE movie_no = :n'
    cursor.execute(stmt, {'r': rank, 'n': movie_no})
    conn.commit()
    cursor.close()
    conn.close