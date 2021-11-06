import networkx as nx
import Environment_V1
import Data_manager_V1
import random


env = Environment_V1.LogisticNetwork()
data = Data_manager_V1.DataManager()

time_max = int(input('max time : '))


def path_finder(dep, arv):
    path = list()
    path.append(env.hub_data[dep][3])
    path.append('중부권 광역우편물류센터')
    path.append(env.hub_data[arv][3])
    return path

# 1 시간단위 = 15분
# 허브 통과 : 메인허브(6시간) / 서브허브(3시간)


env.reset_network('data/data_road_V3.csv', 'data/data_hub_V3.csv')

for time in range(time_max):
    data.sample_maker(env.hub_ground_codes, random.randint(10, 40), time)
    for key in data.parcel.keys():            # sample = [코드, 상태, 진행단계, 완료단계]
        # Ground, Road, Hub
        if data.parcel[key][0] == 'G':        # 출발지 또는 도착지
            if not data.parcel[key][3][0][1]:       # 출발 안 했을 경우
                path = path_finder(data.parcel[key][3][0][0], data.parcel[key][3][-1][0])
                data.parcel[key][3][1][0] = path[0]
                data.parcel[key][3][2][0] = path[1]
                data.parcel[key][3][3][0] = path[2]
                data.parcel[key][0] = 'R'
                data.parcel[key][3][0][1] = True
                data.parcel[key][2] = nx.shortest_path_length(env.network, data.parcel[key][3][0][0], data.parcel[key][3][1][0])
                env.traffic[env.hub_data[data.parcel[key][3][0][0]][4]][env.hub_data[data.parcel[key][3][1][0]][4]] += 1
            else:                                   # 배송 완료되었을 경우
                data.parcel[key][3][4][1] = True
                data.parcel_log[key][3][1] = time
                del data.parcel[key]
        elif data.parcel[key][0] == 'R':        # 도로 주행중
            if data.parcel[key][1] == data.parcel[key][2]:      # 도로 운송 완료됨
                for i in range(1,4):
                    if not data.parcel[key][3][i][1]:
                        env.hub_load(data.parcel[key][3][i][0], key)
                        break
                        # 허브 하차
            else:
                data.parcel[key][1] += 1

    for key in data.parcel.keys():
        for i in range(4):
            if not data.parcel_cost[key][i]:
                data.parcel_cost[key][i] = env.traffic[env.hub_data[data.parcel[key][3][0][0]][4]][env.hub_data[data.parcel[key][3][1][0]][4]]
    for key in env.hub_sky_codes:
        done = env.hub_classification(key)
        for k in done:
            data.parcel[k][0] = 'R'
            # 허브 상차

data.save_log('HnS_simulation_21104_01')
