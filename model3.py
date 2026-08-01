import numpy as np
import pandas as pd

from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score

df = pd.read_csv("jj_train0.csv", header=None)

y_raw = df.iloc[:, 0].values
x_raw = df.iloc[:, 1:].values

x_train, x_test, y_train_raw, y_test_raw = train_test_split(x_raw, y_raw, test_size=0.031, shuffle=False)

rf = RandomForestRegressor(
    n_estimators=100,
    max_depth=None,
    random_state=42
)

rf.fit(x_train, y_train_raw)

y_pred = rf.predict(x_test)
mse = mean_squared_error(y_test_raw, y_pred)
rmse = np.sqrt(mse)
r2 = r2_score(y_test_raw, y_pred)

print(f"RMSE: {rmse:.2f}")
print(r2)

for i in range(10):
    print(rf.predict([x_test[i]]))