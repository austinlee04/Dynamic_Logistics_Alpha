import random
import csv
from collections import deque
from Environment_V1 import LogisticNetwork
# try to use pandas

env = LogisticNetwork()

MAX = 10 ** 4


class DataManager:
    def __init__(self):
        self.parcel = dict()            # code : [state, dep, arv, route]
        self.parcel_log = dict()

    def sample_maker(self, nodes, num, time):
        for i in range(1, num+1):
            parcel_code = format(time, '03')+'P'+str(MAX + i)
            dep, arv = random.sample(nodes, 2)
            self.parcel[parcel_code] = ['G', 0, [dep, False], deque([[arv, False]]), [0, 0]]
            # [3].append left [경유지, 통과여부]
            # [위치, 도로운송완료시간, [경로[위치, 도착여부]], 도착지, 현재 경로]
            self.parcel_log[parcel_code] = [[dep, time], [arv, 0], deque(), []]
            # [2].append [경유지, 도착시간, 출발시간] --> 허브 통과 정보
            # [3].append [출발지, 도착지, 거리, 구간 통행량] --> 도로 통과 정보

    def save_log(self, name):

        f = open('HnS_simulation/'+name+'.csv', 'w', newline='')
        wr = csv.writer(f)

        wr.writerow(['택배번호',
                     '출발지', '출발시간',
                     '경유지1', '하차시간', '상차시간', '거리', '통행량',
                     '경유지2', '하차시간', '상차시간', '거리', '통행량',
                     '경유지3', '하차시간', '상차시간', '거리', '통행량',
                     '도착지', '도착시간', '거리', '통행량'])

        for key in self.parcel_log.keys():
            data = list()
            data.append(key)                                    # 택배번호
            data.extend(self.parcel_log[key][0])                # 출발지, 출발시간
            if len(self.parcel_log[key][2]) >= 1:
                data.extend(self.parcel_log[key][2][0])         # 경유지1, 하차시간, 상차시간
                data.extend(self.parcel_log[key][3][0][2:])     # 거리, 통행량
            if len(self.parcel_log[key][2]) >= 2:
                data.extend(self.parcel_log[key][2][1])         # 경유지2, 하차시간, 상차시간
                data.extend(self.parcel_log[key][3][1][2:])     # 거리, 통행량
            if len(self.parcel_log[key][2]) >= 3:
                data.extend(self.parcel_log[key][2][2])         # 경유지3, 하차시간, 상차시간
                data.extend(self.parcel_log[key][3][2][2:])     # 거리, 통행량
            data.extend(self.parcel_log[key][1])                # 도착지, 도착시간
            data.extend(self.parcel_log[key][3][3][2:])         # 거리, 통행량
            wr.writerow(data)

        f.close()
