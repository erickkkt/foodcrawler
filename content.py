import numpy as np
import pandas as pd

import sklearn
from sklearn.neighbors import NearestNeighbors

cars = pd.read_csv('mtcars.csv')
cars.columns = ['car_names', 'mpg', 'cyl', 'disp', 'hp', 'drat', 'wt', 'qsec', 'vs', 'am', 'gear', 'carb']
a = cars.head()
# print(a)

t = [15,300, 160, 3.2]
X = cars.ix[:,(1,3,4,6)].values
a = X[0:5]
# print(a)

nbrs = NearestNeighbors(n_neighbors=1).fit(X)
# print(nbrs.kneighbors([t]))

print(cars)
