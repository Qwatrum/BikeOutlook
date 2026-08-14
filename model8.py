import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
import lightgbm as lgb
from sklearn.metrics import classification_report

def run(file, num):
    df = pd.read_csv(file, header=None)

    df[15] = df[15].astype('category')
    X = df.drop(columns=[0])
    y = df[0]

    X.columns = X.columns.astype(str)
    num_classes = num

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1, shuffle=False)

    # scaler = StandardScaler()
    # scaler.fit(X_train)
    # X_train = scaler.transform(X_train)
    # X_test = scaler.transform(X_test)

    params = {
        "objective": "multiclass",
        "num_class": num_classes,
        "metric": "multi_logloss",
        "verbose": 0
    }

    train_data = lgb.Dataset(X_train, label=y_train)
    test_data = lgb.Dataset(X_test, label=y_test, reference=train_data)

    num_round = 100
    model = lgb.train(params, train_data, num_round, valid_sets=[test_data])
    y_p = model.predict(X_test, num_iteration=model.best_iteration)
    y_pred = np.argmax(y_p, axis=1)
    accuracy = accuracy_score(y_test, y_pred)

    return accuracy
