import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import cx_Oracle as oc
import os
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.metrics.pairwise import linear_kernel, cosine_similarity

# # Oracle Connection
# os.environ["NLS_LANG"] = ".AL32UTF8"
# START_VALUE = u"Unicode \u3042 3".encode('utf-8')
# END_VALUE = u"Unicode \u3042 6".encode('utf-8')
#
# conn = oc.connect('hyeminseo/hyeminseo@203.236.209.97:1521/XE')
# cursor = conn.cursor()
# cursor.execute('select * from movie')
# # print(cursor.fetchall())
# # for rs in cursor:
# #     print(rs)
#
# cursor.close()
# conn.close

movie = pd.read_csv('movie_dt.csv')
movie['MOVIE_CONTENT'] = movie['MOVIE_CONTENT'].fillna('')
# print(movie['MOVIE_CONTENT'])

# 영화 설명 벡터화
tf = TfidfVectorizer(analyzer='word', ngram_range=(1,2), min_df=0, stop_words='english')
tf_matrix = tf.fit_transform(movie['MOVIE_CONTENT'])
# print(tf_matrix)

# tf_matrix 간의 유사성 계산
cos_sim = linear_kernel(tf_matrix, tf_matrix)
# print(cos_sim[0])

# 데이터 정제
movie = movie.reset_index()
titles = movie['MOVIE_TITLE']
idxs = pd.Series(movie.index, index=titles)

# 영화 제목을 매개변수로 비슷한 영화 10개를 추천해주는 함수
def getRecom(title):
    idx = idxs[title]
    sim_scores = list(enumerate(cos_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x:x[1], reverse=True)
    sim_scores = sim_scores[1:11]
    movie_idx = [i[0] for i in sim_scores]
    print(titles.iloc[movie_idx])
    return titles.iloc[movie_idx]

getRecom('호텔 뭄바이')