import pandas as pd
import numpy as np
import xgboost as xgb

from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score

def run(file):
    df = pd.read_csv(file, header=None)

    df.iloc[:, 15] = df.iloc[:,15].astype('category')

    X_raw = df.iloc[:, 1:]
    y = df.iloc[:, 0]
    for col in X_raw.columns:
        if X_raw[col].dtype == 'object':
            X_raw[col] = X_raw[col].astype('category')

    X_train, X_test, y_train, y_test = train_test_split(X_raw, y, test_size=0.1, shuffle=False)

    model = xgb.XGBRegressor(objective='reg:squarederror', n_estimators=100, enable_categorical=True, random_state=42)
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)

    r2 = r2_score(y_test, y_pred)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    # print(f"RMSE: {rmse:.4f}")
    # print(f"r2: {r2:.4f}")

    return rmse, r2
