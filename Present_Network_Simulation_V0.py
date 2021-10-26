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
    for key in data.parcel.keys():            # sample = [코드, 상태, 진행단계, 완료단계]
        if data.parcel[key][0] == 'G':
            if not data.parcel[key][3][0][1]:
                data.parcel[key][0] = 'R'
                data.parcel[key][3][0][1] = True
                data.parcel_log[key][1][1] = time
        if sample[1] == 'R':
            road.move(sample[0])
            if sample[1] < sample[2]:
                sample[1] += 1
            else:
                pass
                # 허브 과정으로(하차)
        elif sample[1] == 'H':
            if sample[1] == 'W':
                pass
                # 대기중
            else:
                if sample[1] < sample[2]:
                    sample[1] += 1
                else:
                    pass
                    # 상차