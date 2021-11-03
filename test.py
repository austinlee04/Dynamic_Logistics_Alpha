import csv

f = open('data_road_V1.csv','r',encoding='UTF-8')
data = csv.reader(f)

next(data)
name = list()
dist = list()
edge = list()
n = 1

for row in data:
    if n == 1:
        for value in row:
            if value:
                name.append(value)
    else:
        for value in row:
            if value:
                dist.append(value)
        for i in range(1, len(name)):
            if dist[i] == '0':
                continue
            edge.append([name[i-1], name[i], float(dist[i])])
        name = []
        dist = []

    n *= -1

for i in edge:
    print(i)



