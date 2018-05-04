import pandas as pd
import numpy as np
import sklearn
from sklearn.decomposition import TruncatedSVD

columns = ['user_id', 'item_id', 'rating', 'timestamp']
frame = pd.read_csv('ml-100k/u.data', sep = '\t', names=columns)
# print(frame.head())

columns = ['item_id', 'movie title', 'release date', 'video release date', 'IMDb URL', 'unknown', 'Action',
           'Adventure', 'Animation', ' Childrens', 'Comedy', 'Crime', 'Documentary', 'Drama', 'Factasy', 'Film-Noir', 'Horror',
           'Musical', 'Mystery', 'Romance', 'Sci-Fi', 'Thriller', 'War', 'Western']
movies = pd.read_csv('ml-100k/u.item', sep='|', names=columns, encoding='latin-1')
movie_names = movies[['item_id','movie title']]
# print(movie_names.head())

combined_movies_data = pd.merge(frame, movie_names, on = 'item_id')
# print(combined_movies_data.head())

t = combined_movies_data.groupby('item_id')['rating'].count().sort_values(ascending=False).head()
# print(t)

filter = combined_movies_data['item_id'] == 50
a = combined_movies_data[filter]['movie title'].unique()
# print(a)

ratings_crosstab = combined_movies_data.pivot_table(values='rating', index='user_id', columns='movie title', fill_value = 0)
# print(rating_crosstab.head())

b = ratings_crosstab.shape
# print(b)

X = ratings_crosstab.values.T
a = X.shape
print(a)

SVD = TruncatedSVD(n_components=12, random_state=17)
resultant_matrix = SVD.fit_transform(X)
a = resultant_matrix.shape
# print(a)

corr_mat = np.corrcoef(resultant_matrix)
a = corr_mat.shape
# print(a)

movies_names = ratings_crosstab.columns
movies_list = list(movie_names)
# print(movies_list)
star_wars = movies_list.index('Star Wars (1977)')
print(star_wars)

