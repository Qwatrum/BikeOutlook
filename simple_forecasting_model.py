import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import mean_squared_error
import xgboost as xgb
from sklearn.model_selection import TimeSeriesSplit


df = pd.read_csv("trainJuneJulyCleaned2.csv")
df = df.set_index("timestamp")

# df = df.drop("is_weekend", axis=1)
df = df.drop("weekday", axis=1)
df = df.drop(columns=df.columns[2:])
df.index = pd.to_datetime(df.index)
"""
df_lag = df.copy()
df_lag = df_lag.drop(index='2026-05-24 16:00:00')
df_lag = df_lag.reset_index()
df = df.reset_index()


d_df = df.copy()

d_df['delta'] = df_lag['306149925'] - df['306149925']
print(d_df.head())

d_df = d_df.set_index("timestamp")
d_df.index = pd.to_datetime(d_df.index)


df = df.set_index("timestamp")
df.index = pd.to_datetime(df.index)

# train = df.loc[df.index < '13-07-2026']
# test = df.loc[df.index >= '13-07-2026']

# df.loc[(df.index > '13-07-2026') & (df.index < '21-07-2026')].plot()
# plt.show()

def create_time_features(df):
    df = df.copy()
    df['minute'] = df.index.minute
    df['hour'] = df.index.hour
    df['dayofweek'] = df.index.dayofweek
    df['dayofyear'] = df.index.dayofyear
    return df
d_df = create_time_features(d_df)
fig, ax = plt.subplots(figsize=(10, 8))
sns.boxplot(data=d_df, x='dayofweek', y='delta')
# plt.show()
"""




# plt.show()

def create_time_features(df):
    df = df.copy()
    df['minute'] = df.index.minute
    df['hour'] = df.index.hour
    df['dayofweek'] = df.index.dayofweek
    df['dayofyear'] = df.index.dayofyear
    return df


def add_lags(df):
    df = df.copy()
    target_map = df['306149925'].to_dict()
    df['lag8'] = (df.index - pd.Timedelta('8 hours')).map(target_map)
    df['lag12'] = (df.index - pd.Timedelta('12 hours')).map(target_map)
    df['lag16'] = (df.index - pd.Timedelta('16 hours')).map(target_map)

    return df

df = add_lags(df)

tss = TimeSeriesSplit(n_splits=6, test_size=4*8, gap=2)
df = df.sort_index()
fig, axs = plt.subplots(6, 1, figsize=(15,15), sharex=True)
fold = 0
preds = []
scores = []

for train_idx, val_idx in tss.split(df):
    train = df.iloc[train_idx]
    test = df.iloc[val_idx]
    train = create_time_features(train)
    test = create_time_features(test)

    features = ["minute", "hour", "dayofweek", "dayofyear", "lag8", "lag12", "lag16"]
    target = "306149925"
    train['306149925'].plot(ax=axs[fold], label="Training SEt", title=f"Data train test split fold {fold}")
    test['306149925'].plot(ax=axs[fold], label="test SEt")
    axs[fold].axvline(test.index.min(), color='black', ls='--')

    

    
    x_train = train[features]
    y_train = train[target]
    x_test = test[features]
    y_test = test[target]


    reg = xgb.XGBRegressor(n_estimators=100, early_stopping_rounds = 20, learning_rate=0.01, booster='gbtree', objective='reg:linear', max_depth=5, base_score=0.5)


    reg.fit(x_train, y_train, eval_set=[(x_train, y_train), (x_test, y_test)], verbose=100)


    fold += 1




plt.show()