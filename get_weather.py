import csv

with open("wetterdaten_15min.csv") as file:
    lines = csv.reader(file)

    hour_before = 0
    minute_before = "00"
    b = {"00":"45", "15":"00", "30":"15", "45":"30"}
    for i, l in enumerate(lines):
        if i != 0:
            time = l[0].split(";")[1]
            hour = time.split(":")[0]
            minute = time.split(":")[1]

            flag = False

            if minute_before != b[minute]:
                print(l)


            minute_before = minute
