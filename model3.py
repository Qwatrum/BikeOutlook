import numpy as np
import pandas as pd

from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score, accuracy_score, precision_score, f1_score, recall_score

df = pd.read_csv("jj_train0_a_c_m.csv", header=None)

y_raw = df.iloc[:, 0].values
x_raw = df.iloc[:, 1:].values

x_train, x_test, y_train_raw, y_test_raw = train_test_split(x_raw, y_raw, test_size=0.1, shuffle=False)

rf = RandomForestRegressor(
    n_estimators=100,
    max_depth=12,
    random_state=42
)

rf.fit(x_train, y_train_raw)

y_pred = rf.predict(x_test)
mse = mean_squared_error(y_test_raw, y_pred)
rmse = np.sqrt(mse)
r2 = r2_score(y_test_raw, y_pred)
accuarcy = accuracy_score(y_test_raw, y_pred)


print(f"RMSE: {rmse:.4f}")
print(f"r2: {r2:.4f}")
print(f"Accuracy: {accuarcy:.4f}")

'''
print(x_test[-11])
for i in range(-11,1,1):
    print(rf.predict([x_test[i]]))'''