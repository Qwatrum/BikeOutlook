import csv
import math


filename = "trainJuneJulyCleaned.csv"

snapshots = []



fieldnames = ["in_15", "month_sin", "month_cos", "day_sin", "day_cos", "weekend", "weather", "hour_sin", "hour_cos"]
data = []
current_station = 0

def feature_to_sine_cosine(feature, I):
    s = 2*math.pi / (I[-1]+1-I[0])
    v = s * feature

    return round(math.sin(v),4), round(math.cos(v), 4)


with open(filename, "r") as file:
    lines = list(csv.reader(file))

for station in ['306149925', '306150652', '306151680', '306152946', '306153381', '306154042', '306155298', '306155771', '306157005', '306157498', '306159446', '306424741', '306426180', '306427898', '306427940', '306429471', '306429774', '306430168', '306430513', '306432156', '306434837', '306435831', '306436482', '306437759', '306584215', '306586739', '306589353', '306591040', '306592207', '306608230', '306611557', '306612767', '306614385', '306615251', '306616745', '306618340', '306619536', '306621528', '306632182', '306633317', '306634776', '306636890', '306637891', '306638803', '306641629', '306642669', '306644874', '306646326', '306647862', '307167971', '340929155', '349238105', '491528970', '491529093', '494484950', '498525578', '498527077', '501685208', '501686803', '502500548', '502644017', '503111106', '503112749', '503913022', '503913656', '504159382', '504161296', '508767590', '508797016', '510452084', '510661082', '510668681', '510669510', '510823763', '511030440', '511031589', '511032542', '511033558', '511746900', '511748258', '511750351', '512964246', '512979792', '513312395', '513313081', '513313802', '513369212', '515857745', '518186274', '518187588', '518188627', '518189709', '522790447', '524003076', '524251504', '526095217', '535580393', '549361281', '560798726', '560799825', '562880614', '562881229', '562882007', '563250095', '563251452', '563252736', '563255058', '563255677', '563917827', '563962959', '600959781', '606704630', '606705162', '607882729', '607883109', '607883401', '610254646', '611851824', '611900524', '612091846', '621820081', '621821180', '621871253', '622029184', '629549986']:
    fieldnames.append(f"station_{station}_before_30")
    fieldnames.append(f"station_{station}_before_15")
    fieldnames.append(f"station_{station}_current")
#print(fieldnames)
for i, line in enumerate(lines[3:-3]):
    print(line)

    day = int(line[1])
    day_sin, day_cos = feature_to_sine_cosine(day, [0,6])
    is_weekend = int(line[2])
    month = int(line[0].split(" ")[0].split("-")[1])
    month_sin, month_cos = feature_to_sine_cosine(month, [1,12])

    hour = int(line[0].split(" ")[1].split(":")[0])
    
    hour_sin, hour_cos = feature_to_sine_cosine(hour, [0, 23])

    weather = 0

    new_data = []

    # predict more than 15
    # new_data.append(int(lines[i+3+3][current_station+3])) # plus three because start with third line
    # new_data.append(int(lines[i+2+3][current_station+3]))
    # absolute
    new_data.append(int(lines[i+1+3][current_station+3]))

    # change of station
    # new_data.append(int(lines[i+1+3][current_station+3]) - int(lines[i+3][current_station+3]))
    #new_data.extend([month_sin, month_cos, day_sin, day_cos, is_weekend, weather, hour_sin, hour_cos])
    new_data.extend([hour_sin, hour_cos])

    

    for j, station in enumerate(line[3:]):
        # absolute
        new_data.append(round(int(lines[i-2+3][j+3])))
        new_data.append(round(int(lines[i-1+3][j+3])))
        new_data.append(round(int(station)))

        # delta
        # new_data.append(int(lines[i-1+3][j+3])-int(lines[i-2+3][j+3]))
        # new_data.append(int(station) - int(lines[i-1+3][j+3]))
    
    data.append(new_data)

#print(data)

with open(f"jj_train{current_station}.csv", "w", newline='') as file:
    writer = csv.writer(file)

    writer.writerows(data)