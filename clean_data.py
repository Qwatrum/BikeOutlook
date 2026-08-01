import csv
from datetime import datetime, timedelta

filename = "data/trainJuneJuly.csv"


with open(filename, "r") as file:
    lines = list(csv.reader(file))


for i, e in enumerate(lines.copy()):
    for j, l in enumerate(e):
        '''

        todo substract two hours in app
        
        
        if i!=0 and j == 0:
            l2 = l.split(" ")
            l21 = l2[0].split("-")
            l22 = l2[1].split(":")
            before = datetime(int(l21[0]), int(l21[1]), int(l21[2]), int(l22[0]), int(l22[1]), int(l22[2]))
            lines[i][j] = str(before + timedelta(hours=2))

        '''
        if l == '':
            lines[i][j] = '0'

print(lines[0])

with open(f"{filename.split("/")[-1].removesuffix(".csv")}Cleaned.csv", "w", newline='') as file:

    writer = csv.writer(file)

    writer.writerows(lines)
