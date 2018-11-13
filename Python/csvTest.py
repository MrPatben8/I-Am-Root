import csv

with open("Desktop/precipitacion2014-csv.csv", "r" ) as f :
    reader = csv.reader(f)
    for row in reader:
        print (row[0])
