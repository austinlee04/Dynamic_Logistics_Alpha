import Environment_V1
import Data_manager_V1
import networkx as nx
import random
from tqdm import tqdm
from collections import deque

env = Environment_V1.LogisticNetwork()
data = Data_manager_V1.DataManager()

time_max = int(input('max time : '))
speed = 15


def path_finder(dep, arv):
    path = list()
    path.append(env.hub_data[dep][3])
    path.append('중부권 광역우편물류센터')
    path.append(env.hub_data[arv][3])
    return path

# 1 시간단위 = 15분
# 허브 통과 : 메인허브(6시간) / 서브허브(3시간)


env.reset_network('data/data_road_V3.csv', 'data/data_hub_V3.csv')

for time in tqdm(range(1, time_max+1)):
    data.sample_maker(env.hub_ground_codes, random.randint(10, 40), time)
    for key in data.parcel.keys():            # sample = [코드, 상태, 진행단계, 완료단계]
        # Ground, Road, Hub
        if data.parcel[key][0] == 'G':        # 출발지 또는 도착지
            if not data.parcel[key][2][1]:       # 출발 안 했을 경우
                path = deque(path_finder(data.parcel[key][2][0], data.parcel[key][3][-1][0]))
                path_ = deque(reversed(path))
                for i in range(len(path_)):
                    data.parcel[key][3].appendleft([path_[i], False])
                    data.parcel_log[key][2].appendleft([path_[i], 0, 0])
                data.parcel[key][0] = 'R_'
                data.parcel[key][2][1] = True

                if len(data.parcel[key][3]) > 1:        # 경유지 존재 case
                    path.appendleft(data.parcel[key][2][0])
                    path.append(data.parcel[key][3][-1][0])
                    for i in range(len(path)-1):
                        data.parcel_log[key][3].append([path[i], path[i+1], 0, 0])
                    data.parcel_log[key][3][0][2] = round(nx.shortest_path_length(env.network, data.parcel[key][2][0], data.parcel[key][3][0][0], weight='weight'))
                    data.parcel_log[key][2][0][1] = time + round(data.parcel_log[key][3][0][2] / speed)
                    data.parcel[key][1] = time + data.parcel_log[key][3][0][2]
                    data.parcel[key][4][0] = env.hub_data[data.parcel[key][2][0]][4]
                    data.parcel[key][4][1] = env.hub_data[data.parcel[key][3][-1][0]][4]
                    env.traffic[data.parcel[key][4][0]][data.parcel[key][4][1]] += 1

                else:                   # 경유지 존재X case (=직통배송) --> HnS sim 에서는 사용X
                    data.parcel_log[key][3].append([data.parcel[key][2][0], data.parcel[key][3][-1][0], 0, 0])
                    data.parcel_log[key][3][0][2] = round(nx.shortest_path_length(env.network, data.parcel[key][2][0], data.parcel[key][3][-1][0], weight='weight') / speed)
                    data.parcel[key][1] = time + data.parcel_log[key][3][0][2]
                    data.parcel[key][4][0] = env.hub_data[data.parcel[key][2][0]][4]
                    data.parcel[key][4][1] = env.hub_data[data.parcel[key][3][-1][0]][4]
                    env.traffic[data.parcel[key][4][0]][data.parcel[key][4][1]] += 1

            else:                                   # 배송 완료되었을 경우
                data.parcel_log[key][1][1] = time
                del data.parcel[key]
        elif data.parcel[key][0] == 'R':        # 도로 주행중
            if data.parcel[key][1] == time:      # 도로 운송 완료됨
                for i in range(len(data.parcel[key][3])-1):
                    if not data.parcel[key][3][i][1]:
                        env.hub_load(data.parcel[key][3][i][0], time, key)
                        data.parcel[key][3][i][1] = True
                        if i == len(data.parcel[key][3]) - 1:
                            data.parcel[key][0] = 'G'
                            data.parcel_log[key][1][1] = time
                        else:
                            data.parcel[key][0] = 'H'
                            data.parcel_log[key][2][i][1] = time
                        env.traffic[data.parcel[key][4][0]][data.parcel[key][4][1]] -= 1
                        break
                        # 간선하차

    for key in env.hub_sky_codes:
        done = env.hub_classification(key, time)
        if not done:
            continue
        for k in done:
            for i in range(1, len(data.parcel_log[k][2])):
                if not data.parcel[k][3][i][1] and i == len(data.parcel_log[k][2]):     # 최종 경유지 통과(마지막 운송)
                    data.parcel[k][0] = 'R_'
                    data.parcel[k][3][i][1] = True
                    data.parcel_log[k][2][i-1][2] = time
                    data.parcel_log[k][3][i][2] = round(nx.shortest_path_length(env.network, data.parcel[k][2][-1][0], data.parcel[k][3][0], weight='weight'))
                    data.parcel[k][1] = time + round(data.parcel_log[k][3][i][2] / speed)
                elif not data.parcel[k][3][i][1]:
                    data.parcel[k][0] = 'R_'
                    data.parcel[k][3][i][1] = True
                    data.parcel_log[k][3][i-1][2] = round(nx.shortest_path_length(env.network, data.parcel[k][3][i-1][0], data.parcel[k][3][i][0], weight='weight'))
                    data.parcel[k][1] = time + round(data.parcel_log[k][3][i][2] / speed)
                    data.parcel_log[k][2][-1][2] = time
                    data.parcel[k][4][0] = env.hub_data[data.parcel_log[k][2][i-1][0]][4]
                    data.parcel[k][4][1] = env.hub_data[data.parcel_log[k][2][i][0]][4]
                    env.traffic[data.parcel[k][4][0]][data.parcel[k][4][1]] += 1
                # 간선상차

    for key in data.parcel.keys():
        if data.parcel[key][0] == 'R_':
            for i in range(len(data.parcel_log[key][3])):
                if not data.parcel_log[key][3][i][3]:
                    data.parcel_log[key][3][i][3] = env.traffic[data.parcel[key][4][0]][data.parcel[key][4][1]]
                    data.parcel[key][0] = 'R'
                    # print(data.parcel_log[key])
                    break

# for key in data.parcel_log.keys():
  #  print(key, data.parcel_log[key])


#data.save_log('HnS_simulation_211107_06')
