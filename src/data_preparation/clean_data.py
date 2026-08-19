import csv
from datetime import datetime, timedelta

filename = "data_preparation/trainJuneJuly.csv"


with open(filename, "r") as file:
    lines = list(csv.reader(file))


for i, e in enumerate(lines.copy()):
    for j, l in enumerate(e):
        
        
        
        
        if i!=0 and j == 0:
            date = datetime.strptime(l, "%Y-%m-%d %H:%M:%S")
            dt2 = date + timedelta(hours=2)
            out = dt2.strftime("%Y-%m-%d %H:%M:%S")
            lines[i][j] = out

        
        if l == '':
            lines[i][j] = '0'

print(lines[0])

with open(f"{filename.split("/")[-1].removesuffix(".csv")}Cleaned.csv", "w", newline='') as file:

    writer = csv.writer(file)

    writer.writerows(lines)
