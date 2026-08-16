import pandas as pd
import numpy as np
from sklearn.metrics import r2_score, mean_squared_error
import matplotlib.pyplot
#df = pd.read_csv('juneJuly_ava_8.csv', header=None)

"""x = df[20]
x = (x > 0).astype(int)
y = df[0]
# 20 current
print(np.sqrt(mean_squared_error(y, x)))
print(r2_score(y, x))
df = pd.read_csv('juneJuly_ava_12.csv', header=None)


x = df[20]
x = (x > 0).astype(int)
y = df[0]
# 20 current
print(np.sqrt(mean_squared_error(y, x)))
print(r2_score(y, x))"""

df = pd.read_csv('juneJuly_abs_24_L.csv', header=None)

x = df[20]
y = df[0]

#print(x[0])
print(np.sqrt(mean_squared_error(y, x)))
print(r2_score(y, x))

df = pd.read_csv('juneJuly_c_24_L.csv', header=None)
y = df[0]
# y.plot(kind='hist', edgecolor='black')
# matplotlib.pyplot.hist(y, bins=5, color='black')
# matplotlib.pyplot.show()
conditions = [
    df[20] == 0,
    df[20] == 1,
    df[20].isin([2, 3]),
    df[20].isin([4, 5, 6])
]

choices = [0, 1, 2, 3]

x = np.select(conditions, choices, default=4)
print(np.sqrt(mean_squared_error(y, x)))
print(r2_score(y, x))

