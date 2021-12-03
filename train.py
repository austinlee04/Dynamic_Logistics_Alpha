from Present_Network_Simulation_V3 import Simulation
from Agent_REINFORCE_V0 import Agent
import numpy as np

if __name__ == "__main__":
    state_size = 24
    # 각 허브의 포화도
    actions = [(0,0,0),(1,0,0),(0,1,0),(0,0,1),(1,1,0),(1,0,1),(0,1,1),(1,1,1)]
    # 0은 허브 패싱, 1은 허브 통과
    action_size = len(actions)
    agent = Agent(state_size, action_size)
    sim = Simulation()

    scores, episodes = [],[]
    episode_num = int(input('how many episodes? : '))

    for e in range(episode_num):
        done = False
        score = 0

        sim.env.reset_network('data/data_road_V3.csv', 'data/data_hub_V3.csv')
        state = sim.get_state()
        state = np.reshape(state, [1, state_size])


        while not done:
