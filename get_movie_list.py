import pandas as pd
import cx_Oracle as oc
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

# 회원 번호를 매개변수로 가장 최근 좋아요를 누른 작품명을 반환
def getTitle(no):
    os.environ["NLS_LANG"] = ".AL32UTF8"
    START_VALUE = u"Unicode \u3042 3".encode('utf-8')
    END_VALUE = u"Unicode \u3042 6".encode('utf-8')

    conn = oc.connect('hyeminseo/hyeminseo@localhost:1521/XE')
    cursor = conn.cursor()
    cursor.execute('select movie_title from movie where movie_no in (select movie_no from (select rownum, movie_no from '
                   '(select movie_no from good where member_no = ' + str(no) + ' and movie_good > 0 order by good_date desc) where rownum = 1))')

    title = cursor.fetchone()[0]
    cursor.close()
    conn.close
    return title

# 영화 content를 기반으로 유사한 영화 12편 추천
def getRecom(title):
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

    # 영화 제목을 매개변수로 비슷한 영화 12편을 추천해주는 함수
    idx = idxs[title]
    sim_scores = list(enumerate(cos_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x:x[1], reverse=True)
    sim_scores = sim_scores[1:13]
    movie_idx = [i[0] for i in sim_scores]
    recom_list = list(movie.iloc[movie_idx]['MOVIE_NO'])
    return recom_list

# 추천 영화 12편의 movie_no를 list로 반환
def getList(no):
    title = getTitle(no)
    list = []

    if title != '' and title != None:
        mv_list = getRecom(title)
        if len(mv_list) > 0:
            for mv in mv_list:
                inner_list = []
                os.environ["NLS_LANG"] = ".AL32UTF8"
                START_VALUE = u"Unicode \u3042 3".encode('utf-8')
                END_VALUE = u"Unicode \u3042 6".encode('utf-8')

                conn = oc.connect('hyeminseo/hyeminseo@localhost:1521/XE')
                cursor = conn.cursor()
                cursor.execute('select * from movie where movie_no =' + str(mv) + '')
                for rs in cursor:
                    for r in rs:
                        if type(r) == str:
                            r = r.replace('\xa0', ' ')
                            r = r.replace('\u200b', ' ')
                        inner_list.append(r)
                    list.append(inner_list)
                cursor.close()
                conn.close
            return list
    else:
        return list