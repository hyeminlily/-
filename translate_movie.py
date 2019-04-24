import pandas as pd

movies = pd.read_csv('movie.csv', sep=',', engine='python', encoding='utf-8')
print(movies.iloc[1:-1])