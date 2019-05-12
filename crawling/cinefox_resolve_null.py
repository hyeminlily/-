from bs4 import BeautifulSoup
import cx_Oracle as oc
import os
import requests
import re

# Oracle Connection - insert
os.environ["NLS_LANG"] = ".AL32UTF8"
START_VALUE = u"Unicode \u3042 3".encode('utf-8')
END_VALUE = u"Unicode \u3042 6".encode('utf-8')

conn = oc.connect('hyeminseo/hyeminseo@203.236.209.97:1521/XE')
cursor = conn.cursor()
cursor.execute('select movie_no from movie where movie_content is null')
conn.commit()

null_list = []
for no in cursor:
    null_list.append(no[0])

for movie_no in null_list:
    url = 'http://clean.cinefox.com/vod/view?product_seq=' + str(movie_no)
    result = requests.get(url=url, timeout=10)
    data = BeautifulSoup(result.content, 'html.parser')

    div_cont = data.find('div', {'id': "content"})
    if div_cont is None:
        content = '<br>'
    elif div_cont.text.strip() == '':
        content = '<br>'
    else:
        text = div_cont.text.strip()
        content = re.sub('\t|\r|\n', '', text)
        content = content.replace('    ', '')

        content = content.replace('. ', '.<br>')
        content = content.replace('<br>.<br>', '<br>')
        content = content.replace('.<br>.<br>.<br>', '.<br>')
        content = content.replace('.<br>.<br>.<br>.<br>', '.<br>')
        content = content.replace('.<br>.<br>.<br>.<br>.<br>', '.<br>')
        content = content.replace('.<br>.<br>.<br>.<br>.<br>.<br>', '.<br>')

    q = "UPDATE movie SET movie_content = :c WHERE movie_no = :n"
    cursor.execute(q, (content, movie_no))
    conn.commit()

cursor.close()
conn.close
