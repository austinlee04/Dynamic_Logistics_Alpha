import networkx as nx
import csv
from collections import deque

'''
허브 DATA : self.hub_data[코드][대기열, 최대용량, 이름, 처리시간]
배송 DATA : [고유번호][출발지, 도착지, 경유지(list)]
'''


class LogisticNetwork:
    def __init__(self):
        self.network = nx.Graph()
        self.data_road = list()
        self.data_hub = list()
        self.hub_num = 0
        self.hub_data = {}
        self.hub_ground_codes = list()
        self.hub_sky_codes = list()
        self.traffic = list()

    def reset_network(self, road_file, hub_file):            # 시뮬레이션 초기화             ## 구현 완료
        f1 = open(road_file, 'r', encoding='UTF-8')
        f2 = open(hub_file, 'r', encoding='UTF-8')
        self.data_road = csv.reader(f1)
        self.data_hub = csv.reader(f2)
        next(self.data_hub)
        for row in self.data_hub:
            self.hub_data[row[0]] = [deque(), int(row[1]), int(row[4]), row[2], int(row[5])]
            # 이름:[대기열, 최대용량, 처리시간, 상위허브, 번호]
            self.network.add_edge(row[0], row[3].split()[1], weight=15)
            if row[1] == '0':
                self.hub_ground_codes.append(row[0])
            else:
                self.hub_sky_codes.append(row[0])
        self.hub_num = len(self.hub_data.keys())
        self.traffic = [[0 for _ in range(self.hub_num)] for _ in range(self.hub_num)]
        # [출발지][도착지]

        name = list()
        dist = list()
        n = 1
        for row in self.data_road:
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
                    self.network.add_edge(name[i - 1], name[i], weight=float(dist[i]))
                name = []
                dist = []

            n *= -1

    def update_weight(self):    # 교통상황 반영       -->  추후 예정(필수 X)
        pass

    def solve_path_cost(self, path, path_len):     # 경로 비용 계산   ## 구현 완료
        cost = 0
        for i in range(path_len-1):
            cost += nx.shortest_path_length(self.network, source=path[i], target=path[i+1], weight='weight')
        return cost

# 허브에서의 이동 관련 함수들

    def hub_load(self, hub, sample):
        self.hub_data[hub][0].append([sample, 0])

    def hub_classification(self, hub):
        done = list()
        for i in range(self.hub_data[hub][1]):
            if not self.hub_data[hub][0][i]:
                return
            elif self.hub_data[hub][0][i][1] == self.hub_data[hub][2]:
                done.append(self.hub_data[hub][0].popleft()[0])
                # 허브 탈출
            else:
                self.hub_data[hub][0][i][1] += 1
        return done
