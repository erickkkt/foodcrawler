import numpy as np
import pandas as pd

from pandas import Series, DataFrame
from sklearn.linear_model import LinearRegression
from sklearn.metrics import classification_report

bank_full = pd.read_csv('bank_full_w_dummy_vars.csv')
a = bank_full.head()
# print(a)

b = bank_full.info()
print(b)
