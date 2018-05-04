import numpy as np
import pandas as pd

frame = pd.read_csv('rating_final.csv')
cuisine = pd.read_csv('chefmozcuisine.csv')
geodata = pd.read_csv('geoplaces2.csv', encoding='latin-1')

# print(frame.head())

# print(geodata.head())

places = geodata[['placeID','name']]
# print(places.head())

# print(cuisine.head())

rating = pd.DataFrame(frame.groupby('placeID')['rating'].mean())
# print(rating.head())

rating['rating_count'] = pd.DataFrame(frame.groupby('placeID')['rating'].count())
# print(rating.head())

# print(rating.describe())

# print(rating.sort_values('rating_count', ascending=False).head())

# print(places[places['placeID'] == 135085])
# print(cuisine[cuisine['placeID'] == 135085])

places_crosstab = pd.pivot_table(data=frame, values='rating', index='userID', columns='placeID')
# print(places_crosstab.head())

Tortas_ratings = places_crosstab[135085]
# print(Tortas_ratings[Tortas_ratings >= 0])

similar_to_Tortas = places_crosstab.corrwith(Tortas_ratings)
corr_Tortas = pd.DataFrame(similar_to_Tortas, columns=['PearsonR'])
corr_Tortas.dropna(inplace=True)
print(corr_Tortas.head())

Tortas_corr_summary = corr_Tortas.join(rating['rating_count'])
print(Tortas_corr_summary[Tortas_corr_summary['rating_count'] >= 10].sort_values('PearsonR', ascending=False).head(10))

places_corr_Tortas = pd.DataFrame([135085, 132754, 135045, 135062, 135028, 135042, 135046], index=np.arange(7), columns=['placeID'])
summary = pd.merge(places_corr_Tortas, cuisine, on='placeID')
# print(summary)

# print(places[places['placeID'] == 135046])

# print(cuisine['Rcuisine'].describe())






