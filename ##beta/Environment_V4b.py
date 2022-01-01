import networkx as nx
from collections import deque
import numpy as np
import pandas as pd


class LogisticNetwork:
    def __init__(self):
        self.network = nx.Graph()
        self.hub_num = 0
        self.hub_data = dict()
        self.hub_ground_codes = np.array([])
        self.hub_sky_codes = np.array([])
        self.traffic = np.array([])
        self.volume = np.array([])

    def network_settings(self, road_file, hub_file):            # 시뮬레이션 초기 설정
        f1 = pd.read_csv(road_file, encoding='UTF-8')
        f2 = pd.read_csv(hub_file, encoding='UTF-8', header=None)
        data_road = f1.to_numpy()
        data_hub = f2.to_numpy()
        for row in data_hub:
            self.hub_data[row[0]] = [deque(), int(row[1])*10, int(row[4]), row[2], int(row[5])]
            # 이름:[대기열, 처리용량, 처리시간, 상위허브, 번호]
            self.network.add_edge(row[0], row[3].split()[1], weight=15.0)
            if row[1] == '0':
                np.append(self.hub_ground_codes, row[0])
            else:
                np.append(self.hub_sky_codes, row[0])
        self.hub_num = self.hub_ground_codes.size + self.hub_sky_codes.size
        self.traffic = np.zeros((self.hub_num+1, self.hub_num+1), dtype=np.int64)
        # [출발지][도착지]
        for name in self.hub_sky_codes:
            np.append(self.volume, self.hub_data[name][1])

        for row in data_road:
            self.network.add_edge(row[0], row[1], weight=round(float(row[2])))

    def reset_network(self):        # 시뮬레이션 초기화
        for name in self.hub_sky_codes:
            self.hub_data[name][0] = deque()
        # 교통상황을 반영할 시, network 업데이트 과정을 여기 추가!!!

# 허브에서의 이동기들(E)
    def hub_load(self, hub, time, sample):
        if len(self.hub_data[hub][0]) <= self.hub_data[hub][1]:
            self.hub_data[hub][0].append([sample, time+self.hub_data[hub][2]])
        else:
            self.hub_data[hub][0].append([sample, 0])

    def hub_classification(self, hub, time):
        done = list()
        k = 0
        for i in range(self.hub_data[hub][1]):
            if not self.hub_data[hub][0] or len(self.hub_data[hub][0]) <= k:
                break
            if self.hub_data[hub][0][0][1] == time:
                done.append(self.hub_data[hub][0].popleft()[0])
            elif not self.hub_data[hub][0][k][1]:
                self.hub_data[hub][0][k][1] = time + self.hub_data[hub][2]
                k += 1
        return done
