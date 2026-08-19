import csv
import math
import pandas
import random
def main(category, tr, for_nn, less_info, oversampled, o_rate):
    input_file = "data/trainJuneJulyCleaned2.csv"
    output_file = "juneJuly"
    c = ""
    categories = category
    train_start = int(24 * 60 / 15) # 24h

    train_predict = tr
    station_ids = [306149925,306150652,306151680,306152946,306153381,306154042,306155298,306155771,306157005,306157498,306159446,306424741,306426180,306427898,306427940,306429471,306429774,306430168,306430513,306432156,306434837,306435831,306436482,306437759,306584215,306586739,306589353,306591040,306592207,306608230,306611557,306612767,306614385,306615251,306616745,306618340,306619536,306621528,306632182,306633317,306634776,306636890,306637891,306638803,306641629,306642669,306644874,306646326,306647862,307167971,340929155,349238105,491528970,491529093,494484950,498525578,498527077,501685208,501686803,502500548,502644017,503111106,503112749,503913022,503913656,504159382,504161296,508767590,508797016,510452084,510661082,510668681,510669510,510823763,511030440,511031589,511032542,511033558,511746900,511748258,511750351,512964246,512979792,513312395,513313081,513313802,513369212,515857745,518186274,518187588,518188627,518189709,522790447,524003076,524251504,526095217,535580393,549361281,560798726,560799825,562880614,562881229,562882007,563250095,563251452,563252736,563255058,563255677,563917827,563962959,600959781,606704630,606705162,607882729,607883109,607883401,610254646,611851824,611900524,612091846,621820081,621821180,621871253,622029184,629549986]

    # helper
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

    def to_category(v):
        # Returns the category of the amount of available bicycles
        return 0 if v == 0 else (1 if v==1 else (2 if v in [2,3] else (3 if v in [4,5,6] else 4)))

    def to_availability(v):
        # Returns if at least one bike is available
        return 1 if v > 0 else 0
    
    weather = {}
    with open("data/weatherdata.csv", "r", encoding='utf-8') as file:
        lines = list(csv.reader(file))
        for line in lines[1:]:

            va = [line[1], line[2], line[3], line[4], line[5], line[6], line[7]]

            weather[line[0]] = va

    equal_predicts = {0: 0, 1: 0}

    data = []
    input_data = []
    with open(input_file, "r") as file:
        lines = list(csv.reader(file))

    for line in lines[1:]:
        input_data.append(line)

    for j, moment in enumerate(input_data[train_start+1:len(input_data)-train_predict]):
            assert len(station_ids) == len(moment) - 3
            row = get_times(moment[0], moment[1], moment[2])
            if for_nn:
                row.pop(0)
                row.pop(0)
                row.pop(2)
                row.pop(5)
                row.pop(5)
                row.pop(5)

            weather_currently = weather[moment[0]]
            
            row.append(int(round(float(weather_currently[0])))) # temperature in °C
            row.append(int(weather_currently[1])) # humidity
            row.append(float(weather_currently[2])) # rain

            row.append(int(weather_currently[3])) # weather code

            row.append(int(round(float(weather_currently[4])))) # air pressure
            row.append(int(round(float(weather_currently[5])))) # wind speed
            row.append(int(round(float(weather_currently[6])))) # cloud

            for i, id in enumerate(station_ids):
                new_row = row.copy()

                if not for_nn:
                    new_row.append(str(id))

                if categories["absolute"] == 1:
                    target_amount = int(input_data[train_start+1 +j +train_predict][i +3])
                    # these statements check whether the target val is equal to the current value, just for checking the models accuracy
                    if target_amount == int(moment[i +3]):
                        equal_predicts[1] += 1
                    else:
                        equal_predicts[0] += 1
                    c = "abs"
                elif categories["available"] == 1:
                    target_amount = to_availability(int(input_data[train_start+1 +j +train_predict][i +3]))
                    if target_amount == to_availability(int(moment[i +3])):
                        equal_predicts[1] += 1
                    else:
                        equal_predicts[0] += 1
                    c = "ava"
                elif categories["categorical"] == 1:
                    v = int(input_data[train_start+1 +j +train_predict][i +3])
                    v1 = int(moment[i +3])
                    target_amount = to_category(v)
                    if target_amount == to_availability(v1):
                        equal_predicts[1] += 1
                    else:
                        equal_predicts[0] += 1
                    c = "c"
                elif categories["change"] == 1:
                    target_amount = int(input_data[train_start+1 +j +train_predict][i +3]) - int(input_data[train_start+1 +j][i +3])
                    if target_amount == int(moment[i +3]) - int(input_data[train_start+1 +j -train_predict][i +3]):
                        equal_predicts[1] += 1
                    else:
                        equal_predicts[0] += 1
                    c = "d"
                else:
                    print("NO TARGET CATEGORY SET !")
                    quit()
                new_row.insert(0, target_amount)
                
                
                current_amount = int(moment[i +3])
                fifteen_ago = int(input_data[train_start+1 +j -1][i +3])
                thrity_ago = int(input_data[train_start+1 +j -2][i +3])
                forty_five_ago = int(input_data[train_start+1 +j -3][i +3])
                sixty_ago = int(input_data[train_start+1 +j -4][i +3])
                two_ago = int(input_data[train_start+1 +j -8][i +3])
                day_ago = int(input_data[train_start+1 +j -96][i +3])
                new_row.append(current_amount)
                new_row.append(fifteen_ago)
                new_row.append(thrity_ago)
                new_row.append(forty_five_ago)
                new_row.append(sixty_ago)
                new_row.append(two_ago)
                new_row.append(day_ago)

                new_row.append(current_amount-fifteen_ago)
                new_row.append(current_amount-thrity_ago)
                new_row.append(current_amount-forty_five_ago)
                new_row.append(current_amount-sixty_ago)
                new_row.append(current_amount-two_ago)

                new_row.append(round((current_amount+fifteen_ago+thrity_ago)/3, 4))
                new_row.append(round((current_amount+fifteen_ago+thrity_ago+forty_five_ago+sixty_ago)/5, 4))

                df = pandas.Series([current_amount, fifteen_ago, thrity_ago, forty_five_ago, sixty_ago])
                new_row.append(round(float(df.std(ddof=0)),4))

                moments_int = [int(x) for x in moment[3:]]
                others_int = [int(x) for x in input_data[train_start+1 +j -1][3:]]
                others_int2 = [int(x) for x in input_data[train_start+1 +j -2][3:]]
                new_row.append(sum(moments_int))
                new_row.append(sum(moments_int)-sum(others_int))

                others_int.pop(i)
                others_int2.pop(i)
                moments_int.pop(i)

                if less_info == 0:
                    for k in range(len(others_int)):
                        new_row.append(moments_int[k])
                        new_row.append(moments_int[k] - others_int[k])
                        new_row.append(others_int[k] - others_int2[k])

                if oversampled == 1:
                    if target_amount != to_availability(current_amount):
                        data.append(new_row)
                    elif random.randint(0, 100) > o_rate:
                        data.append(new_row)
                    else:
                        continue

    
    p = (1 - round(equal_predicts[0] / (equal_predicts[0] + equal_predicts[1]), 2)) * 100
    if abs((o_rate)-p) > 2:
        print("Oversample rate is to off compared to actual distribution")
        print("Recommend Oversample rate: " + str(p))

    nn = "_nn" if for_nn == 1 else ""
    li = "_L" if less_info == 1 else ""
    o = "_o" if oversampled == 1 else ""
    with open(output_file+"_"+c+"_"+str(int(train_predict))+nn+li+o+".csv", "w", encoding='utf-8', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(data)






main({"categorical":0, "absolute": 0, "available": 1, "change": 0}, 4, 0, 1, 1, 99)