import numpy as np
import networkx as nx
import csv
from collections import deque
import random


class LogisticNetwork:
    def __init__(self):
        self.network = nx.Graph()
        f1 = open('road_test_sample.csv', 'r')
        f2 = open('hub_test_sample.csv', 'r')
        self.road_network_data = csv.reader(f1)
        self.hub_data = csv.reader(f2)                      # !허브 관련 정보를 하나의 딕셔너리로 묶어야 함
        self.hub_num = 0
        self.hub_codes = list()
        self.hub_max = list()
        self.hub_name = list()
        self.hub_classification_time = list()
        self.hub_queue = {}

    def reset_network(self):
        next(self.hub_data)
        for row in self.hub_data:
            self.hub_codes.append(row[0])
            self.hub_queue[row[0]] = deque()
            self.hub_max = int(row[1])
            self.hub_name = row[2]
            self.hub_classification_time = row[3]
        self.hub_num = len(self.hub_codes)

    def sample_maker(self, num):        # 무작위로 샘플 생성[출발지, 도착지]      ## 구현 완료
        sample = list()
        for _ in range(num):
            sample.append(random.sample(self.hub_codes, 2))
        return sample

    def update_weight(self):    # 교통상황 반영       -->  추후 예정(필수 X)
        pass

    def solve_path_cost(self, path, path_len):     # 경로 비용 계산   ## 구현 완료
        cost = 0
        for i in range(path_len-1):
            cost += nx.shortest_path_length(self.network, source=path[i], target=path[i+1], weight='weight')
        return cost

class HubProcess(LogisticNetwork):
    def hub_load(self, hub, sample):
        for data in sample:
            self.hub_queue[hub].append([data, 0])

    def hub_classification(self, hub):
        for parcel in self.hub_queue[hub]:
            parcel[0][1] += 1

    def hub_exit(self, hub, ):
        exit = list()
        while True:
            if self.hub_queue[0][1]


class RoadProcess(LogisticNetwork):
    pass
