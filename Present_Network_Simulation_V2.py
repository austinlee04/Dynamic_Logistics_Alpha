import Environment_V2
import Data_manager_V2
import networkx as nx
import random
from tqdm import tqdm
from collections import deque

env = Environment_V2.LogisticNetwork()
data = Data_manager_V2.DataManager()

time_max = int(input('max time : '))
speed = 15


def path_finder(dep, arv):
    waypoint = list()
    waypoint.append(dep)
    waypoint.append(env.hub_data[dep][3])
    waypoint.append('중부권 광역우편물류센터')
    waypoint.append(env.hub_data[arv][3])
    waypoint.append(arv)
    return waypoint

'''
1시간단위 = 15분
허브 통과시간 : 
    메인허브(중부권 광역우편물류센터) = 6시간(24) 
    서브허브(중부권 광역우편물류센터 외) = 3시간(12)
'''

env.reset_network('data/data_road_V3.csv', 'data/data_hub_V3.csv')

for time in tqdm(range(1, time_max+1)):
    data.sample_maker(env.hub_ground_codes, random.randint(10, 40), time)

    for key in data.parcel.keys():
        # Ground(경로 설정 해야 함), Road, Hub, Finished
        if data.parcel[key][0] == 'G':
            path = path_finder(data.parcel[key][4][0][0], data.parcel[key][4][-1][0])
            for i in range(1, len(path)-1):
                data.parcel[key][4][i+1][0] = path[i]
                data.parcel_log[key][0][i][0] = path[i]
            road_path = [i for i in path if not '']
            for i in range(0, len(road_path)-1):
                length = round(nx.shortest_path_length(env.network, road_path[i], road_path[i+1], weight='weight'))
                data.parcel_log[key][1].append([road_path[i], road_path[i+1], length, 0])




