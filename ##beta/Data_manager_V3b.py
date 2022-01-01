import random
import pandas as pd
from Environment_V4_ import LogisticNetwork

env = LogisticNetwork()
MAX = 10 ** 4


class DataManager:
    def __init__(self):
        self.parcel = dict()            # code : [state, dep, arv, route]
        self.parcel_log = pd.DataFrame()

    def sample_maker(self, nodes, num, time):
        key = list()
        for i in range(1, num+1):
            parcel_code = format(time, '03')+'P'+str(MAX + i)
            dep, arv = random.sample(nodes, 2)
            if (dep, arv) not in key:
                key.append((dep, arv))
            self.parcel[parcel_code] = ['G', 0, [0, 0], [[dep, '', '', '', arv], [0, 0, 0, 0]]]
            # pd.DataFrame 사용...?????????????? (쓰고 싶기는 함)
            # [위치, 도로운송완료시간, [경로 출발지 번호, 경로 도착지 번호], [[경유지], [경유지간 거리(0일 경우 이미 지나감)]]]
            # [3].append left [경유지, 통과여부]
        return key

    def reset_log(self):
        self.parcel = dict()
        self.parcel_log = pd.Dataframe(columns=['code', 'n(WP)',
                                                'DT 0', 'DEP', 'DIS 0', 'TRAFFIC 0',
                                                'AT 1', 'WP 1', 'DT 1', 'DIS 1', 'TRAFFIC 1',
                                                'AT 2', 'WP 2', 'DT 2', 'DIS 2', 'TRAFFIC 2',
                                                'AT 3', 'WP 3', 'DT 3', 'DIS 3', 'TRAFFIC 3',
                                                'AT 4', 'ARV',
                                                'SPD', 'COST', 'EF'])

    def save_log(self, name):
        self.parcel_log.to_csv('HnS_simulation/'+name+'.csv')
        # header=False, index=False
