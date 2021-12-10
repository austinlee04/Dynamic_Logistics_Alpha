from Environment_V3 import LogisticNetwork
from Data_manager_V2 import DataManager
import networkx as nx
import random


class Simulation(LogisticNetwork, DataManager):
    def __init__(self):
        super(LogisticNetwork, self).__init__()
        super(DataManager, self).__init__()
        self.time_max = int(input('max time : '))
        self.speed = 15
        self.env = LogisticNetwork()
        self.data = DataManager()
        self.weight = list()
        self.routes = list()

    def get_state(self, time):
        self.routes = self.data.sample_maker(self.env.hub_ground_codes, random.randint(100, 400), time)
        state = []
        for sample in self.routes:
            s = list()
            s.append(round(len(self.env.hub_data[self.routes[0]][0]) / self.env.hub_data[self.routes[0]][1] * 100))
            s.append(round(len(self.env.hub_data['중부권 광역우편물류센터'][0]) / self.env.hub_data['중부권 광역우편물류센터'][1] * 100))
            s.append(round(len(self.env.hub_data[self.routes[1]][0]) / self.env.hub_data[self.routes[1]][1] * 100))
            sum = 0
            for name in self.env.hub_sky_codes:
                if name == '중부권 광역우편물류센터':
                    continue
                sum += round(len(self.env.hub_data[name][0]) / 2)
            s.append(round(sum / len(self.env.hub_data['중부권 광역우편물류센터'][1]) * 100))
            state.append(s)
        return state

    def path_finder_weights(self, data):
        # 경로 따른 가중치 설정
        pass

    def path_finder(self, dep, arv):
        waypoint = list()
        waypoint.append(dep)
        waypoint.append(self.env.hub_data[dep][3])
        waypoint.append('중부권 광역우편물류센터')
        waypoint.append(self.env.hub_data[arv][3])
        waypoint.append(arv)
        return waypoint

    def simulate(self, time):
        for key in self.data.parcel.keys():
            # Ground(경로 설정 해야 함), Road(R_ : 도로 배치), Hub, Finished
            if self.data.parcel[key][0] == 'G':
                # 운송정보 초기 설정
                path = self.path_finder(self.data.parcel[key][-1][0], self.data.parcel[key][-1][1])
                # 인공지능 반영할 때 path_finder 함수를 변경할 것!!!
                path = [i for i in path if not '']
                for i in range(len(path)):
                    self.data.parcel[key][3].append([path[i], False])
                    self.data.parcel_log[key][0].append([path[i], 0, 0])
                for i in range(len(path) - 1):
                    self.data.parcel_log[key][1].append([path[i], path[i + 1], round(
                        nx.shortest_path_length(self.env.network, path[i], path[i + 1], weight='weight')), 0])
                del self.data.parcel[key][-1]
                self.data.parcel[key][3][0][1] = True
                self.data.parcel[key][0] = 'R_'

            elif self.data.parcel[key][0] == 'R':
                # 도로 주행
                if self.data.parcel[key][1] == time:
                    for i in range(1, len(self.data.parcel[key][3])):
                        if not self.data.parcel[key][3][i][1]:
                            self.data.parcel[key][3][i][1] = True
                            # print(key, data.parcel[key][3])
                            if self.data.parcel[key][3][-1][1]:
                                self.data.parcel[key][0] = 'F'
                                # print(key)
                                self.data.parcel_log[key][0][-1][1] = time
                            else:
                                self.data.parcel[key][0] = 'H'
                                self.data.parcel_log[key][0][i][1] = time
                                self.env.hub_load(self.data.parcel[key][3][i][0], time, key)
                                self.env.traffic[self.data.parcel[key][2][0]][self.data.parcel[key][2][1]] -= 1
                                break

        for key in list(self.data.parcel.keys()):  # 데이터를 효율적으로 사용하기 위해 운송이 끝난 parcel 의 데이터를 삭제하는 과정
            if self.data.parcel[key][0] == 'F':
                del self.data.parcel[key]

        for name in self.env.hub_sky_codes:
            # 허브에서 간선상차
            done = self.env.hub_classification(name, time)
            if not done:
                continue
            for key in done:
                for i in range(2, len(self.data.parcel[key][3])):
                    print(name, key)
                    if not self.data.parcel[key][3][i][1]:
                        self.data.parcel[key][0] = 'R_'
                        self.data.parcel_log[key][0][i - 1][2] = time
                        break

        for key in self.data.parcel.keys():
            if self.data.parcel[key][0] == 'R_':
                for i in range(1, len(self.data.parcel[key][3])):
                    if not self.data.parcel[key][3][i][1]:
                        self.data.parcel_log[key][0][i - 1][2] = time
                        self.data.parcel[key][2][0] = self.env.hub_data[self.data.parcel[key][3][i - 1][0]][4]
                        self.data.parcel[key][2][1] = self.env.hub_data[self.data.parcel[key][3][i][0]][4]
                        self.env.traffic[self.data.parcel[key][2][0]][self.data.parcel[key][2][1]] += 1
                        break

        for key in self.data.parcel.keys():
            if self.data.parcel[key][0] == 'R_':
                for i in range(1, len(self.data.parcel[key][3])):
                    if not self.data.parcel[key][3][i][1]:
                        self.data.parcel[key][1] = time + round(self.data.parcel_log[key][1][i - 1][2] / 15)
                        self.data.parcel_log[key][1][i - 1][3] = self.env.traffic[self.data.parcel[key][2][0]][self.data.parcel[key][2][1]]
                        self.data.parcel[key][0] = 'R'
                        break

    def arrival(self):
        pass

    def get_result(self):
        states = [0, 0, 0, 0]
        return states

    def save_simulation(self):
        self.data.save_log('HnS_simulation_211129_03')
