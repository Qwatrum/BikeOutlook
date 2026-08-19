import pandas as pd
from xgboost import XGBClassifier
from xgboost import plot_tree
import matplotlib.pyplot as plt 
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.metrics import (
    balanced_accuracy_score, f1_score, classification_report,
    confusion_matrix
)
import numpy as np

weather_cat_col = 16
baseline_col = 21

def eval_vs_baseline(y_test, y_pred, baseline_pred, label=""):
    y_test = np.array(y_test)
    y_pred = np.array(y_pred)

    baseline_pred = np.array(baseline_pred)
    changed = (y_test != baseline_pred)
    unchanged = ~changed

    print()
    print(f"Modell-Accuracy without d:  {accuracy_score(y_test[unchanged], y_pred[unchanged]):.4f}")
    print()
    print(f"Modell-Accuracy with d:  {accuracy_score(y_test[changed], y_pred[changed]):.4f}")
    
def to_category(v):
    return 0 if v == 0 else (1 if v==1 else (2 if v in [2,3] else (3 if v in [4,5,6] else 4)))

def to_availability(v):
    return 1 if v > 0 else 0

def run(file):
    df = pd.read_csv(file, header=None)

    #df.iloc[:, 15] = df.iloc[:,15].astype('category')

    X_raw = df.iloc[:, 1:]
    
    X_raw.isetitem(weather_cat_col, X_raw.iloc[:, weather_cat_col].astype('category'))

    y = df.iloc[:, 0]
    for col in X_raw.columns:
        if X_raw[col].dtype == 'object':
            X_raw[col] = X_raw[col].astype('category')

    X_train, X_test, y_train, y_test = train_test_split(X_raw, y, test_size=0.1, shuffle=False)

    xgb_c = XGBClassifier(enable_categorical=True, max_depth=11, learning_rate=0.1, n_estimators=100)
    xgb_c.fit(X_train, y_train)
    # print(len(X_test.iloc[-1, :].values))
    #xgb_c.save_model("model.bst")
    y_pred = xgb_c.predict(X_test)
    baseline_raw_current = X_test.iloc[:, baseline_col].values
    # print(baseline_raw_current[:4])
    baseline_pred = np.array([to_availability(v) for v in baseline_raw_current])
    #print(baseline_raw_current[1:3])
    accuracy = accuracy_score(y_test, y_pred)

    eval_vs_baseline(y_test, y_pred, baseline_pred, "a")
    """print("Accuracy:", accuracy_score(y_test, y_pred))
    print("Balanced Accuracy:", balanced_accuracy_score(y_test, y_pred))
    print("Macro F1:", f1_score(y_test, y_pred, average='macro'))
    print("Weighted F1:", f1_score(y_test, y_pred, average='weighted'))
    print(classification_report(y_test, y_pred, zero_division=0))
    print(confusion_matrix(y_test, y_pred))"""

    showcasex = X_test.iloc[[-9]]
    showcasex2 = X_test.iloc[[-1]]
    #print(showcasex)
    print(xgb_c.predict_proba(showcasex))
    print(xgb_c.predict_proba(showcasex2))

    #plt.figure(figsize=(30, 120))
    #plot_tree(xgb_c, num_trees=1)
    #plt.show()
    #booster = xgb_c.get_booster()
    #dumps = booster.get_dump(with_stats=True, dump_format="text")
    #print(dumps[0])
    return accuracy

run("juneJuly_ava_12_L_o.csv")
#run("juneJuly_c_12_L_o.csv")


# oversampled ava 12 data:
# no d: 80 with 62
