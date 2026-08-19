import pandas as pd
from xgboost import XGBClassifier
import xgboost as xgb
import requests
import math
from fastapi import FastAPI

app = FastAPI()

filename = "station_data.csv"

weather_url = "https://api.open-meteo.com/v1/forecast?latitude=52.38&longitude=9.74&current=rain,weather_code,cloud_cover,temperature_2m,relative_humidity_2m,surface_pressure,wind_speed_10m&forecast_days=1"
current_col = 21
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

    if stationId not in [306149925,306150652,306151680,306152946,306153381,306154042,306155298,306155771,306157005,306157498,306159446,306424741,306426180,306427898,306427940,306429471,306429774,306430168,306430513,306432156,306434837,306435831,306436482,306437759,306584215,306586739,306589353,306591040,306592207,306608230,306611557,306612767,306614385,306615251,306616745,306618340,306619536,306621528,306632182,306633317,306634776,306636890,306637891,306638803,306641629,306642669,306644874,306646326,306647862,307167971,340929155,349238105,491528970,491529093,494484950,498525578,498527077,501685208,501686803,502500548,502644017,503111106,503112749,503913022,503913656,504159382,504161296,508767590,508797016,510452084,510661082,510668681,510669510,510823763,511030440,511031589,511032542,511033558,511746900,511748258,511750351,512964246,512979792,513312395,513313081,513313802,513369212,515857745,518186274,518187588,518188627,518189709,522790447,524003076,524251504,526095217,535580393,549361281,560798726,560799825,562880614,562881229,562882007,563250095,563251452,563252736,563255058,563255677,563917827,563962959,600959781,606704630,606705162,607882729,607883109,607883401,610254646,611851824,611900524,612091846,621820081,621821180,621871253,622029184,629549986]:
        return [404]
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
    model24 = XGBClassifier(enable_categorical=True, max_depth=11, learning_rate=0.1, n_estimators=100)
    model4.load_model("src/model/model4.bst")
    model8.load_model("src/model/model8.bst")
    model12.load_model("src/model/model12.bst")
    model24.load_model("src/model/model24.bst")
    p_04 = model4.predict_proba(X).tolist()
    p_08 = model8.predict_proba(X).tolist()
    p_12 = model12.predict_proba(X).tolist()
    p_24 = model24.predict_proba(X).tolist()
    return [current, p_04, p_08, p_12, p_24]



def input_data(stationId: int):

    df = pd.read_csv(filename)

    df.fillna(0, inplace=True)
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
