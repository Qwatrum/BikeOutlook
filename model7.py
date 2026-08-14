import pandas as pd
from xgboost import XGBClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score


def run(file):
    df = pd.read_csv(file, header=None)

    df.iloc[:, 15] = df.iloc[:,15].astype('category')

    X_raw = df.iloc[:, 1:]
    y = df.iloc[:, 0]
    for col in X_raw.columns:
        if X_raw[col].dtype == 'object':
            X_raw[col] = X_raw[col].astype('category')

    X_train, X_test, y_train, y_test = train_test_split(X_raw, y, test_size=0.1, shuffle=False)

    xgb_c = XGBClassifier(enable_categorical=True)
    xgb_c.fit(X_train, y_train)

    y_pred = xgb_c.predict(X_test)

    accuracy = accuracy_score(y_test, y_pred)

    return accuracy