from sklearn.ensemble import RandomForestClassifier
import pandas as pd
import numpy
from sklearn.model_selection import train_test_split

df = pd.read_csv("jj_train0_a_c_m.csv", header=None)

y_raw = df.iloc[:, 0].values
x_raw = df.iloc[:, 1:].values

x_train, x_test, y_train_raw, y_test_raw = train_test_split(x_raw, y_raw, test_size=0.05, shuffle=False)

rf = RandomForestClassifier(n_estimators=100, random_state=42)

rf.fit(x_train, y_train_raw)

print(f"acc: {rf.score(x_test, y_test_raw):.4f}")
print(f"Feature importanc: {rf.feature_importances_}")

#rf.predict(x_test[-2])
print(x_test[1])
for i in range(-30,1):
    print(rf.predict([x_test[i]]))
#print(rf.apply(numpy.reshape(x_test[-2], (1, -1)))) 