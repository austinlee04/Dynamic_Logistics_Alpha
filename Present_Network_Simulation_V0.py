import Environment_V0
import Data_manager
import random


env = Environment_V0.LogisticNetwork()
hub = Environment_V0.HubProcess()
road = Environment_V0.RoadProcess()
data = Data_manager.DataManager()

time_max = int(input('max time : '))

for time in range(time_max):
    data.sample_maker(env.hub_ground_codes, random.randint(10**4, 10**5), time)
    for sample in data.parcel:            # sample = [코드, 상태, 진행단계, 완료단계]
        if sample[0] == 'R':
            road.move(sample[0])
            if sample[1] < sample[2]:
                sample[1] += 1
            else:
                pass
                # 허브 과정으로(하차)
        elif sample[0] == 'H':
            if sample[1] == 'W':
                pass
                # 대기중
            else:
                if sample[1] < sample[2]:
                    sample[1] += 1
                else:
                    pass
                    # 상차
        elif sample[0] == 'G':
            if sample[3] == sample[4]:
                pass
                # 배송 완료
            else:       # 배송 시작
                pass
                # 상차
