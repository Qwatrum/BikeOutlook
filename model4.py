import pandas as pd
from tensorflow import keras
import numpy as np
from keras.models import Sequential
from keras.layers import Input, Dense, Dropout

from sklearn.model_selection import train_test_split
from tensorflow.keras.utils import to_categorical

df = pd.read_csv("jj_train0_m.csv", header=None)

y_raw = df.iloc[:, 0].values
x_raw = df.iloc[:, 1:].values

x_train, x_test, y_train_raw, y_test_raw = train_test_split(x_raw, y_raw, test_size=0.03, shuffle=False)

y_train = to_categorical(y_train_raw, num_classes=28)
y_test = to_categorical(y_test_raw, num_classes=28)


model = Sequential()
model.add(Input(shape=(383,)))
model.add(Dense(130, activation='relu'))
model.add(Dense(32, activation='relu'))
model.add(Dense(28, activation='softmax'))


model.compile(keras.optimizers.Adam(learning_rate=0.001),
              loss='categorical_crossentropy',
              metrics=['accuracy'])

model.fit(x_train, y_train, epochs=8, batch_size=32)

evaluation = model.evaluate(x_test, y_test)

print(evaluation)

showcase = x_test[-3]
showcase_x = showcase[np.newaxis, :]
v = model(showcase_x)

print(v[0])

model.summary()