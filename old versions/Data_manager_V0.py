import random
import csv
from Environment_V0 import LogisticNetwork
# try to use pandas

env = LogisticNetwork()

MAX = 10 ** 6


class DataManager:
    def __init__(self):
        self.parcel = dict()            # code : [state, dep, arv, route]
        self.parcel_expect = dict()
        self.parcel_log = dict()
        self.parcel_cost = dict()

    def sample_maker(self, nodes, num, time):
        for i in range(1,num+1):
            parcel_code = format(time, '03')+'P'+str(MAX + i)
            dep, arv = random.sample(nodes, 2)
            self.parcel[parcel_code] = ['G', 0, 0, [[dep, False], ['',False], ['',False], ['',False], [arv, False]]]
            # [위치, 진행단계, 총 단계, [경로[위치, 완료여부]]
            self.parcel_expect[parcel_code] = [time, dep, arv, 0, ['', 0], ['', 0], ['', 0], 0]
            self.parcel_log[parcel_code] = [[dep, time], ['',0,0,0], ['',0,0,0], ['',0,0,0], [arv, 0, 0], 0]
            # [출발시간, [위치, 도착시간, 출발시간, 구간 통행량], 비용]
            self.parcel_cost[parcel_code] = [0, 0, 0, 0]

    def save_log(self, name):
        f = open(name+'.csv', 'w', newline='')
        wr = csv.writer(f)

        for key in self.parcel_log.keys():
            data = self.parcel_log[key]
            data.extend(self.parcel_cost[key])
            wr.writerow(data)

        f.close()
