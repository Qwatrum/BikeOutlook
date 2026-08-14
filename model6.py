import pandas as pd
import numpy as np
import seaborn as sb
import matplotlib.pyplot as plt
import lightgbm as lgb

from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
from lightgbm import LGBMRegressor

def run(file):
    df = pd.read_csv(file, header=None)
    #df = pd.concat([df, pd.get_dummies(df[15]).astype('int')], axis=1)
    df[15] = df[15].astype('category')
    X = df.drop(columns=[0])
    y = df[0]

    X.columns = X.columns.astype(str)

    X_train, X_test, Y_train, Y_test = train_test_split(X, y, test_size=0.1, shuffle=False)

    # scaler = StandardScaler()
    # X_train = scaler.fit_transform(X_train)
    # X_test = scaler.fit_transform(X_test)

    train_data = lgb.Dataset(X_train, label=Y_train)
    test_data = lgb.Dataset(X_test, label=Y_test, reference=train_data)

    params = {
        "objective": "regression",
        "metric": "rmse",
        "boosting_type": "gbdt",
        "num_leaves": 31,
        "learning_rate": 0.05,
        "feature_fraction": 0.9,
        "verbose": -1
    }


    num_round = 100
    bst = lgb.train(params, train_data, num_boost_round=num_round, valid_sets=[test_data])

    # model = LGBMRegressor(metric="rmse")
    # model.fit(X_train, Y_train)

    y_train = bst.predict(X_train)
    y_test = bst.predict(X_test)

    # print("Training RMSE: ", np.sqrt(mse(Y_train, y_train)))
    # print("Test RMSE: ", np.sqrt(mse(Y_test, y_test)))

    return np.sqrt(mean_squared_error(Y_test, y_test)), r2_score(Y_test, y_test)