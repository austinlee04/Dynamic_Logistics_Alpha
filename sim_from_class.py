from Present_Network_Simulation_V3a import Simulation
import numpy as np
from tqdm import tqdm
import matplotlib.pyplot as plt

# use sim_V3a(takes 5 hubs)
'''
     0=pass, 1=go through
     1:(0,0,0)   2:(1,0,0)   3:(0,1,0)   4:(0,0,1)
     5:(1,1,0)   6:(1,0,1)   7:(0,1,1)   8:(1,1,1)
 '''

if __name__ == "__main__":
    sim = Simulation()
    sim.env.reset_network('data/data_road_V3.csv', 'data/data_hub_V3.csv')

    costs, episodes = [], []
    # max_time = int(input('how much to simulate? :'))
    # MTE = int(input('MTE : '))

    done = 0
    time = 0

    for e in tqdm(range(100)):
    # while done <= MTE:
        time += 1
        sim.get_state(time)
        sim.simulate(time)

    # print(time)
    sim.save_simulation('211218_02_sim(type5)')
