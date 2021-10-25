import networkx as nx
import csv
from collections import deque
import random

'''
허브 DATA : self.hub_data[코드][대기열, 최대용량, 이름, 처리시간]
배송 DATA : [고유번호(1xxxxxx)][출발지, 도착지, 경유지(list)]
'''

class LogisticNetwork:
    def __init__(self):
        self.network = nx.Graph()
        f1 = open('road_test_sample.csv', 'r')
        f2 = open('hub_test_sample.csv', 'r')
        self.data_road_network = csv.reader(f1)
        self.data_hub = csv.reader(f2)
        self.hub_num = 0
        self.hub_data = {}
        self.hub_ground_codes = list()

    def reset_network(self):            # 시뮬레이션 초기화             ## 구현 완료
        next(self.hub_data)
        for row in self.hub_data:
            self.hub_data[row[1]] = [deque(), int(row[2]), row[3], int(row[4])]            # 코드:[대기열, 최대용량, 이름, 처리시간]
            if row[0] == 'G':
                self.hub_ground_codes.append(row[1])
        self.hub_num = len(self.hub_data.keys())

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
            self.hub_data[hub][0].append([data, 0])

    def hub_classification(self, hub):
        for parcel in self.hub_data[hub][0]:
            parcel[0][1] += 1

    def hub_exit(self, hub, ):
        exit = list()
        while True:
            if self.hub_data[hub][1] > self.hub_data[hub]:
                pass



class RoadProcess(LogisticNetwork):
    def hub_route_finder(self, dep, arv):
        

    def route_finder(self):
        pass
