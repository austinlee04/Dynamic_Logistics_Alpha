import random
import csv
from Environment_V1 import LogisticNetwork
# try to use pandas

env = LogisticNetwork()

MAX = 10 ** 6


class DataManager:
    def __init__(self):
        self.parcel = dict()            # code : [state, dep, arv, route]
        self.parcel_log = dict()

    def sample_maker(self, nodes, num, time):
        for i in range(1,num+1):
            parcel_code = format(time, '03')+'P'+str(MAX + i)
            dep, arv = random.sample(nodes, 2)
            self.parcel[parcel_code] = ['G', 0, 0, [[dep, False]], [arv, False]]
            # append [경유지, 통과여부]
            # [위치, 진행단계, 총 단계, [경로[위치, 통과여부]]
            self.parcel_log[parcel_code] = [[dep, time], [arv, 0], [], []]
            # [2] append [경유지, 도착시간, 출발시간]
            # [3] append [출발지, 도착지, 구간 통행량]

    def save_log(self, name):
        f = open(name+'.csv', 'w', newline='')
        wr = csv.writer(f)

        for key in self.parcel_log.keys():
            data = self.parcel_log[key]
            data.extend(self.parcel_cost[key])
            wr.writerow(data)

        f.close()
