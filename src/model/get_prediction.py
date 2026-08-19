import pandas as pd
from xgboost import XGBClassifier
import xgboost as xgb
import requests
import math
from fastapi import FastAPI

app = FastAPI()

filename = "staion_data.csv"

weather_url = "https://api.open-meteo.com/v1/forecast?latitude=52.38&longitude=9.74&current=rain,weather_code,cloud_cover,temperature_2m,relative_humidity_2m,surface_pressure,wind_speed_10m&forecast_days=1"
current_col = 18
def feature_to_sine_cosine(feature, I):
        '''
        Encode feature to sin and cosine
        '''
        s = 2*math.pi / (I[-1]+1-I[0])
        v = s * int(feature)

        return round(math.sin(v),4), round(math.cos(v), 4)

def get_times(time, day_of_week, is_weekend):
        '''
        Return needed times for a given Datetime
        '''
        day_of_week = int(day_of_week)
        is_weekend = int(is_weekend)
        parts = time.split(" ")
        parts1 = parts[0].split("-")
        parts2 = parts[1].split(":")
        year = int(parts1[0])
        month = int(parts1[1])
        month_sin, month_cos = feature_to_sine_cosine(month, [1,12])
        day_sin, day_cos = feature_to_sine_cosine(day_of_week, [0,6])

        hour = int(parts2[0])
        minute = int(parts2[1])
        total_minutes = hour * 60 + minute

        minutes_sin, minutes_cos = feature_to_sine_cosine(total_minutes, [0, 1425])

        return [year, month, month_sin, month_cos, day_of_week, day_sin, day_cos, is_weekend, hour, minute, total_minutes, minutes_sin, minutes_cos]

@app.get("/station/{stationId}")
def get_station_info(stationId: int):

    X = input_data(stationId)
    if X[0] < 0:
        return X
    current = X[current_col]
    X.insert(0, 0)

    X = pd.DataFrame([X])
    X = X.iloc[:, 1:]

    model4 = XGBClassifier(enable_categorical=True, max_depth=11, learning_rate=0.1, n_estimators=100)
    model8 = XGBClassifier(enable_categorical=True, max_depth=11, learning_rate=0.1, n_estimators=100)
    model12 = XGBClassifier(enable_categorical=True, max_depth=11, learning_rate=0.1, n_estimators=100)
    model4.load_model("model4.bst")
    model8.load_model("model8.bst")
    model12.load_model("model12.bst")
    p_04 = model4.predict_proba(X).tolist()
    p_08 = model8.predict_proba(X).tolist()
    p_12 = model12.predict_proba(X).tolist()
    return [current, p_04, p_08, p_12]



def input_data(stationId: int):

    df = pd.read_csv(filename)

    try:
        station_column = df[str(stationId)]

    except KeyError:
        return [-1]

    try:
        request = requests.get(url=weather_url)
        request.raise_for_status()
    except requests.exceptions.HTTPError as err:
        return [-2]
    except requests.exceptions.RequestException as err:
        return [-3]

    try:
        weather = request.json()["current"]
        temperature = int(round(weather["temperature_2m"]))
        humidity = int(weather["relative_humidity_2m"])
        wind_speed = int(round(float(weather["wind_speed_10m"])))
        surface_pressure = int(round(weather["surface_pressure"]))
        rain = float(weather["rain"])
        weather_code = int(weather["weather_code"])
        cloud_cover = int(round(weather["weather_code"]))
    except KeyError:
        return [-4]

    time = df.iloc[-1, 0]
    time_adjusted = pd.to_datetime(time) + pd.Timedelta(hours=2)

    weekday_n = pd.to_datetime(time_adjusted).weekday()
    is_weekend = 0 if weekday_n < 5 else 1

    time_str = time_adjusted.strftime('%Y-%m-%d %H:%M:%S')
    X = get_times(time_str, weekday_n, is_weekend)

    X.append(temperature)
    X.append(wind_speed)
    X.append(humidity)
    X.append(surface_pressure)
    X.append(rain)
    X.append(weather_code)
    X.append(cloud_cover)


    X.append(stationId)

    current_amount = int(station_column.values[-1])
    fifteen_ago = int(station_column.values[-2])
    thrity_ago = int(station_column.values[-3])
    forty_five_ago = int(station_column.values[-4])
    sixty_ago = int(station_column.values[-5])
    two_ago = int(station_column.values[-9])
    day_ago = int(station_column.values[-97])
    X.append(current_amount)
    X.append(fifteen_ago)
    X.append(thrity_ago)
    X.append(forty_five_ago)
    X.append(sixty_ago)
    X.append(two_ago)
    X.append(day_ago)

    X.append(current_amount-fifteen_ago)
    X.append(current_amount-thrity_ago)
    X.append(current_amount-forty_five_ago)
    X.append(current_amount-sixty_ago)
    X.append(current_amount-two_ago)

    X.append(round((current_amount+fifteen_ago+thrity_ago)/3, 4))
    X.append(round((current_amount+fifteen_ago+thrity_ago+forty_five_ago+sixty_ago)/5, 4))

    df2 = pd.Series([current_amount, fifteen_ago, thrity_ago, forty_five_ago, sixty_ago])
    X.append(round(float(df2.std(ddof=0)),4))

    
    X.append(int(df.iloc[-1, 3:].sum()))
    X.append(float(df.iloc[-1, 3:].sum()-df.iloc[-2, 3:].sum()))

    return X
