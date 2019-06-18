
import cx_Oracle as oc
import os

def getInfo(no):
    # Oracle Connection
    os.environ["NLS_LANG"] = ".AL32UTF8"
    START_VALUE = u"Unicode \u3042 3".encode('utf-8')
    END_VALUE = u"Unicode \u3042 6".encode('utf-8')

    conn = oc.connect('hyeminseo/hyeminseo@localhost:1521/XE')
    cursor = conn.cursor()
    cursor.execute('select member_nickname from member where member_no = ' + str(no) + '')
    nickname = cursor.fetchone()[0]

    cursor.execute('select count(distinct(movie_no)) from zzim where member_no = ' + str(no) + ' and movie_zzim > 0')
    cnt_zzim = cursor.fetchone()[0]

    cursor.execute('select count(distinct(movie_no)) from good where member_no = ' + str(no) + ' and movie_good > 0')
    cnt_good = cursor.fetchone()[0]

    cursor.execute('select count(distinct(movie_no)) from bad where member_no = ' + str(no) + ' and movie_bad > 0')
    cnt_bad = cursor.fetchone()[0]

    cursor.close()
    conn.close
    return nickname, cnt_zzim, cnt_good, cnt_bad

