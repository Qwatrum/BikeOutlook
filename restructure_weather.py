import csv
import pandas as pd

with open("weather.csv", "r") as file:
    lines = list(csv.reader(file))

new_lines = []
for i, line in enumerate(lines):
    for j in range(4):

        date = line[0].replace("T", " ") + ":00"
        if j == 0:
            time_adjusted = pd.to_datetime(date) - pd.Timedelta(minutes=15)
            time_str = time_adjusted.strftime('%Y-%m-%d %H:%M:%S')
        elif j == 1:
            time_str = date
        elif j == 2:
            time_adjusted = pd.to_datetime(date) + pd.Timedelta(minutes=15)
            time_str = time_adjusted.strftime('%Y-%m-%d %H:%M:%S')
        elif j == 3:
            time_adjusted = pd.to_datetime(date) + pd.Timedelta(minutes=30)
            time_str = time_adjusted.strftime('%Y-%m-%d %H:%M:%S')

        new_line = [time_str]
        new_line.extend(line[1:])

        new_lines.append(new_line)

with open("weatherdata.csv", "w", newline='') as file:
    writer = csv.writer(file)
    writer.writerows(new_lines)
