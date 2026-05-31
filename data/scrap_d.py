import datetime
import json
import requests
import csv
import os
now = datetime.datetime.now()

t = str(now).split(".")[0]
is_weekend = 0
if now.weekday() == 5 or now.weekday() == 6:
    is_weekend = 1


city_code = "dh"

data = {}
number_of_vehicles = []

filename = "station_data.csv"
try:
    response = requests.get(f"https://gbfs.nextbike.net/maps/gbfs/v2/nextbike_{city_code}/de/station_status.json")
    response.raise_for_status()
    json_data = response.json()
    stations = json_data["data"]["stations"]
except Exception as e:
    print(e)
    stations = []

api_data = {str(s.get("station_id")): s.get("num_bikes_available") for s in stations}
ids = ['306149925', '306150652', '306151680', '306152946', '306153381', '306154042', '306155298', '306155771', '306157005', '306157498', '306159446', '306424741', '306426180', '306427898', '306427940', '306429471', '306429774', '306430168', '306430513', '306432156', '306434837', '306435831', '306436482', '306437759', '306584215', '306586739', '306589353', '306591040', '306592207', '306608230', '306611557', '306612767', '306614385', '306615251', '306616745', '306618340', '306619536', '306621528', '306632182', '306633317', '306634776', '306636890', '306637891', '306638803', '306641629', '306642669', '306644874', '306646326', '306647862', '307167971', '340929155', '349238105', '491528970', '491529093', '494484950', '498525578', '498527077', '501685208', '501686803', '502500548', '502644017', '503111106', '503112749', '503913022', '503913656', '504159382', '504161296', '508767590', '508797016', '510452084', '510661082', '510668681', '510669510', '510823763', '511030440', '511031589', '511032542', '511033558', '511746900', '511748258', '511750351', '512964246', '512979792', '513312395', '513313081', '513313802', '513369212', '515857745', '518186274', '518187588', '518188627', '518189709', '522790447', '524003076', '524251504', '526095217', '535580393', '549361281', '560798726', '560799825', '562880614', '562881229', '562882007', '563250095', '563251452', '563252736', '563255058', '563255677', '563917827', '563962959', '600959781', '606704630', '606705162', '607882729', '607883109', '607883401', '610254646', '611851824', '611900524', '612091846']
existing_ids = []
file_exists = os.path.isfile(filename) and os.path.getsize(filename) > 0

if file_exists:
    with open(filename, "r", newline='') as file:
        reader = csv.reader(file)
        header = next(reader, [])
        if len(header) > 3:
            existing_ids = header[3:]

new_ids = []
for s_id in api_data.keys():
    if s_id not in existing_ids:
        new_ids.append(s_id)
new_ids.sort()
updated_ids = existing_ids + new_ids
fieldnames = ["timestamp", "weekday", "is_weekend"] + updated_ids

if len(new_ids) > 0 and file_exists:
    with open(filename, "r", newline='') as file:
        lines = list(csv.reader(file))
    
    lines[0] = fieldnames
    
    new_count = len(new_ids)
    for i in range(1, len(lines)):
        lines[i].extend([None] * new_count)

    with open(filename, "w", newline='') as file:
        writer = csv.writer(file)
        writer.writerows(lines)

row_dict = {
    "timestamp": t,
    "weekday": now.weekday(),
    "is_weekend": is_weekend
}

for s_id in updated_ids:
    row_dict[s_id] = api_data.get(s_id, None)


with open(filename, "a", newline='') as file:
    writer = csv.DictWriter(file, fieldnames=fieldnames)

    if not file_exists:
        writer.writeheader()

    writer.writerow(row_dict)