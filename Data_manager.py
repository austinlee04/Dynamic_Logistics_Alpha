import random
# try to use pandas

MAX = 10 ** 6

class DataManager:
    def __init__(self):
        self.route_log = dict()
        self.time_log = dict()

    def sample_maker(self, nodes, num, time):
        sample = list()
        for i in range(1,num+1):
            parcel_code = format(time, '03')+'P'+str(MAX + i)
            route = random.sample(self.nodes, 2)
            sample.append(route)
            self.route_log[parcel_code] = [route[0],'','','',route[1],0]
            self.time_log[parcel_code] = [time,0,0,0,0,0,0,0]
        return sample