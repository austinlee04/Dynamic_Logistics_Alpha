import Environment_V0
import Data_manager
import random


env = Environment_V0.LogisticNetwork()
data = Data_manager.DataManager()

time_max = int(input('max time : '))


def path_finder(dep, arv):
    path = list()
    path.append(env.hub_data[dep][3])
    path.append('중부권 광역우편물류센터')
    path.append(env.hub_data[arv][3])
    return path

# 1 시간단위 = 15분
# 허브 통과 : 메인허브(6시간) / 서브허브(3시간)


env.reset_network('data_road.csv', 'data_hub.csv')

for time in range(time_max):
    data.sample_maker(env.hub_ground_codes, random.randint(10**4, 10**5), time)
    for key in data.parcel.keys():            # sample = [코드, 상태, 진행단계, 완료단계]
        # Ground, Road, Hub
        if data.parcel[key][0] == 'G':        # 출발지 또는 도착지
            if not data.parcel[key][3][0][1]:       # 출발 안 했을 경우
                data.parcel[key][0] = 'R'
                data.parcel[key][3][0][1] = True
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
        elif data.parcel[key][0] == 'H':
            pass
            # 허브 처리 과정(env 모듈에서 처리)

data.save_log('HnS_simulation_211030_01')
