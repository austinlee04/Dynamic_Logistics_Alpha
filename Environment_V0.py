import numpy as np
import networkx as nx
import csv
from collections import deque


class LogisticNetwork:
    def __init__(self):
        self.network = nx.Graph()
        f1 = open('.csv', 'r')
        f2 = open('.csv', 'r')
        self.road_network_data = csv.reader(f1)
        self.hub_data = csv.reader(f2)
        self.hub_num = len(self.hub_data)
        self.hub_queue = [deque() for _ in range(self.hub_num)]

    def update_weight(self):    # 교통망 반영
        pass

    def solve_path_cost(self, dep, arv):     # 경로 비용
        pass

    def hub_process(self, hub_id):      # 허브에서 운송 처리 과정 진행
        pass

    def move(self):     # 전체적으로 운송 진행(도로망 + 허브)
        pass