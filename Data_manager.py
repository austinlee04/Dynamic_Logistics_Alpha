import random
# try to use pandas

MAX = 10 ** 6


class DataManager:
    def __init__(self):
        self.parcel = dict()            # code : [state, dep, arv, route]
        self.parcel_expect = dict()
        self.parcel_log = dict()

    def sample_maker(self, nodes, num, time):
        for i in range(1,num+1):
            parcel_code = format(time, '03')+'P'+str(MAX + i)
            dep, arv = random.sample(nodes, 2)
            self.parcel[parcel_code] = ['G', 0, 0, [[dep, False], ['',False], ['',False], ['',False], [arv, False]]]
                                        # [위치, 진행단계, 총 단계, [경로[위치, 완료여부]]
            self.parcel_expect[parcel_code] = [time, dep, arv, ['', 0], ['', 0], ['', 0], 0]
            self.parcel_log[parcel_code] = [[dep, time], ['',0,0], ['',0,0], ['',0,0], [arv, 0], 0]
            # [출발시간, [위치, 도착시간, 출발시간], 비용]

    def route_manager(self):
        for sample in
