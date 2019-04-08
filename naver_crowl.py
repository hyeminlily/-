import cx_Oracle as oc
import os

os.environ["NLS_LANG"] = ".AL32UTF8"
START_VALUE = u"시작값입니다".encode('cp949')
END_VALUE = u"종료값입니다".encode('cp949')

conn = oc.connect('hyeminseo/hyeminseo@203.236.209.97:1521/XE')
cursor = conn.cursor()
cursor.execute('select * from member')
print(cursor.fetchall())

cursor.close()
conn.close