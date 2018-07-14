import numpy as np
import pandas as pd
from scipy.spatial.distance import cosine


places = pd.read_csv('DATA/places.csv')
users = pd.read_csv('DATA/users.csv')
users_new = pd.read_csv('DATA/users-new.csv')

# drop some clumns
places.drop(['link'], axis=1, inplace=True)
places.drop(['address'], axis=1, inplace=True)
places.drop(['open_time'], axis=1, inplace=True)
places.drop(['price_range'], axis=1, inplace=True)

users.drop(['link'], axis=1, inplace=True)
users.drop(['comment'], axis=1, inplace=True)

users_new.drop(['link'], axis=1, inplace=True)
users_new.drop(['comment'], axis=1, inplace=True)

user_concat = pd.concat([users, users_new])

# print(places.head())
# print(users.head())
# print(places[places['name'] == '7 Kỳ Quan - Dimsum & Món Hoa'])
# print(places[places['name'] == 'Amigo Hữu Nghị Restaurant - Beefsteak & Grill'])
def replace_name(x):
    return places[places['placeID']==x].name.values[0]

user_concat.placeID = user_concat.placeID.map(replace_name)

M = user_concat.pivot_table(index=['userID'], columns=['placeID'], values='rating')

def pearson(s1, s2):
    s1_c = s1 - s1.mean()
    s2_c = s2 - s2.mean()
    return np.sum(s1_c * s2_c)/np.sqrt(np.sum(s1_c ** 2) * np.sum(s2_c ** 2))

M.to_csv('DATA/cross_table-raw.csv', sep=',', encoding='utf-8')

# print(M)
# print(M.shape)

# p = pearson(M['Panda BBQ - Xiên Nướng Đồng Giá 5000'], M['Panda BBQ 2 - Xiên Nướng Đồng Giá 5000'])
# print(p)
# print(users.head())

def get_recs(place_name, M, num):
    reviews = []
    for name in M.columns:
        if name == place_name:
            continue
        cor = pearson(M[place_name], M[name])
        if np.isnan(cor):
            continue
        else:
            reviews.append((name, cor))
    reviews.sort(key=lambda tup: tup[1], reverse=True)
    return reviews[:num]

def get_recs_by_cosin(place_name, M, num):
    reviews = []
    for name in M.columns:
        if name == place_name:
            continue
        cor = 1 - cosine(M[place_name], M[name])
        if np.isnan(cor):
            continue
        else:
            reviews.append((name, cor))
    reviews.sort(key=lambda tup: tup[1], reverse=True)
    return reviews[:num]


def get_recs_by_user_id(userID, M, num):
    reviews = []
    for id in M.columns:
        if id == userID:
            continue
        cor = pearson(M[userID], M[id])
        if np.isnan(cor):
            continue
        else:
            reviews.append((id, cor))
    reviews.sort(key=lambda tup: tup[1], reverse=True)
    return reviews[:num]


recs = get_recs('Panda BBQ - Xiên Nướng Đồng Giá 5000', M, 10)
print(recs)

