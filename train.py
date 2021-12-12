from Present_Network_Simulation_V3 import Simulation
from Agent_REINFORCE_V0 import Agent
import numpy as np
from tqdm import tqdm

if __name__ == "__main__":
    state_size = 4
    # 각 허브의 포화도
    actions = [1, 2, 3, 4, 5, 6, 7, 8]
    '''
        0=pass, 1=go through
        1:(0,0,0)   2:(1,0,0)   3:(0,1,0)   4:(0,0,1)
        5:(1,1,0)   6:(1,0,1)   7:(0,1,1)   8:(1,1,1)
    '''
    # 0은 허브 패싱, 1은 허브 통과
    action_size = len(actions)
    agent = Agent(state_size, action_size)
    sim = Simulation()

    scores, episodes = [], []
    episode_num = int(input('how many episodes? : '))
    MTE = 10000     # 에피소드 종료시키기 위해 이동시켜야 하는 소포 양

    for e in tqdm(range(episode_num)):
        done = 0
        score = 0
        time = 1

        sim.env.reset_network('data/data_road_V3.csv', 'data/data_hub_V3.csv')
        state = sim.get_state(time+1)
        # state = np.reshape(state, [1, state_size])

        while done <= MTE:
            for sample in state:
                s = np.reshape(sample, [1, state_size])
                action = agent.get_action(state)

            for result in sim.get_result():
                done += 1
                next_state, action_made, reward = result[0], result[1], result[2]
                next_state = np.reshape(next_state, [1, state_size])
                agent.append_sample(state, action_made, reward)
                score += reward

            time += 1
            state = sim.get_state(time)

        entropy = agent.train_model()
        print("episode: {:3d} | score: {:3d} | entropy: {:.3f}".format(time, score, entropy))
        scores.append(score)
        episodes.append(e)

        agent.model.save_weights('save_model/model', save_format='tf')

    sim.save_simulation('211213_01')
