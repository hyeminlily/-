import pandas as pd
import cinefox_crowl_func

head = ['movie_no', 'movie_title', 'movie_titleEng', 'movie_genre', 'movie_nation', 'movie_runtime', 'movie_grade',
        'movie_opendate', 'movie_director', 'movie_actor', 'movie_fname', 'movie_play_url', 'movie_content']
movies = cinefox_crowl_func.getMovieList()
print(len(movies))
df = pd.DataFrame(movies, index=None, columns=head, dtype='int32')
df.to_csv('movie.csv', encoding='utf-8')
