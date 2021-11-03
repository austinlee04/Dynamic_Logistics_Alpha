import csv

f = open('data_road_test.csv','r','utf-8')
data = csv.reader(f)

for row in data:
    print(row)