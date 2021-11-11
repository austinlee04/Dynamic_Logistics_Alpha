import Environment_V2
import Data_manager_V2
import networkx as nx
import random
from tqdm import tqdm

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
    data.sample_maker(env.hub_ground_codes, random.randint(100, 400), time)

    for key in data.parcel.keys():
        # Ground(경로 설정 해야 함), Road(R_ : 도로 배치), Hub, Finished
        if data.parcel[key][0] == 'G':
            # 운송정보 초기 설정
            path = path_finder(data.parcel[key][-1][0], data.parcel[key][-1][1])
            # 인공지능 반영할 때 path_finder 함수를 변경할 것!!!
            path = [i for i in path if not '']
            for i in range(len(path)):
                data.parcel[key][3].append([path[i], False])
                data.parcel_log[key][0].append([path[i], 0, 0])
            for i in range(len(path)-1):
                data.parcel_log[key][1].append([path[i], path[i+1], round(nx.shortest_path_length(env.network, path[i], path[i+1], weight='weight')), 0])
            del data.parcel[key][-1]
            data.parcel[key][3][0][1] = True
            data.parcel[key][0] = 'R_'

        elif data.parcel[key][0] == 'R':
            # 도로 주행
            if data.parcel[key][1] == time:
                for i in range(1, len(data.parcel[key][3])):
                    if not data.parcel[key][3][i][1]:
                        data.parcel[key][3][i][1] = True
                        # print(key, data.parcel[key][3])
                        if data.parcel[key][3][-1][1]:
                            data.parcel[key][0] = 'F'
                            # print(key)
                            data.parcel_log[key][0][-1][1] = time
                        else:
                            data.parcel[key][0] = 'H'
                            data.parcel_log[key][0][i][1] = time
                            env.hub_load(data.parcel[key][3][i][0], time, key)
                            env.traffic[data.parcel[key][2][0]][data.parcel[key][2][1]] -= 1
                            break

    for key in list(data.parcel.keys()):            # 데이터를 효율적으로 사용하기 위해 운송이 끝난 parcel의 데이터를 삭제하는 과정
        if data.parcel[key][0] == 'F':
            del data.parcel[key]

    for name in env.hub_sky_codes:
        # 허브에서 간선상차
        done = env.hub_classification(name, time)
        if not done:
            continue
        for key in done:
            for i in range(2, len(data.parcel[key][3])):
                if not data.parcel[key][3][i][1]:
                    data.parcel[key][0] = 'R_'
                    data.parcel_log[key][0][i-1][2] = time
                    break

    for key in data.parcel.keys():
        if data.parcel[key][0] == 'R_':
            for i in range(1, len(data.parcel[key][3])):
                if not data.parcel[key][3][i][1]:
                    data.parcel_log[key][0][i-1][2] = time
                    data.parcel[key][2][0] = env.hub_data[data.parcel[key][3][i-1][0]][4]
                    data.parcel[key][2][1] = env.hub_data[data.parcel[key][3][i][0]][4]
                    env.traffic[data.parcel[key][2][0]][data.parcel[key][2][1]] += 1
                    break

    for key in data.parcel.keys():
        if data.parcel[key][0] == 'R_':
            for i in range(1, len(data.parcel[key][3])):
                if not data.parcel[key][3][i][1]:
                    data.parcel[key][1] = time + round(data.parcel_log[key][1][i-1][2] / 15)
                    data.parcel_log[key][1][i-1][3] = env.traffic[data.parcel[key][2][0]][data.parcel[key][2][1]]
                    data.parcel[key][0] = 'R'
                    break


'''
for key in data.parcel.keys():
    print('{}\n{}\n{}\n{}'.format(key, data.parcel[key], data.parcel_log[key][0], data.parcel_log[key][1]))
'''
data.save_log('HnS_simulation_211110_04')

