import cx_Oracle as oc
import os
import pandas as pd
import naverMV_crowl

head = ['movie_no', 'movie_title', 'movie_titleEng', 'movie_genre', 'movie_nation', 'movie_runtime', 'movie_grade',
        'movie_opendate', 'movie_director', 'movie_actor', 'movie_fname', 'movie_play_url', 'movie_content']
movies = naverMV_crowl.getMovieList()
df = pd.DataFrame(movies, index=None, columns=head)
df.to_csv('movie.csv', encoding='utf-8')

# # Oracle Connection
# conn = oc.connect('hyeminseo/hyeminseo@203.236.209.97:1521/XE')
# cursor = conn.cursor()
# cursor.executemany('insert into movie()')
# conn.commit()
# cursor.close()
# conn.close