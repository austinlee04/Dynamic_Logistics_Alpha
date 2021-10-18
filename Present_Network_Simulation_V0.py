import Environment_V0
import random

env = Environment_V0.LogisticNetwork()
hub = Environment_V0.HubProcess()
road = Environment_V0.RoadProcess()

time_max = int(input('max time : '))

for time in range(time_max):
    shipping_data = env.sample_maker(random.randint(50, 800))

