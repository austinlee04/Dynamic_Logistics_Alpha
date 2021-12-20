from Present_Network_Simulation_V3 import Simulation
from Agent_REINFORCE_V0 import Agent
import numpy as np
from tqdm import tqdm
import matplotlib.pyplot as plt

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
    MTE = 750     # 에피소드 종료시키기 위해 이동시켜야 하는 소포 양

    time_taken = list()

    for e in tqdm(range(episode_num)):
    # for e in range(episode_num):
        done = 0
        score = 0
        time = 1

        sim.env.reset_network('data/data_road_V3.csv', 'data/data_hub_V3.csv')


        while done <= MTE:
            state = sim.get_state(time)
            for sample in state:
                route = sample.pop()
                s = np.reshape(sample, [1, state_size])
                action = agent.get_action(s)
                sim.weight[sim.env.hub_data[route[0]][4]-25][sim.env.hub_data[route[1]][4]-25] = action
                # 경로 따른 가중치(행동 선택) 설정

            sim.simulate(time)

            val = sim.get_result()
            if val:
                for result in val:
                    done += 1
                    action_made, reward = result[1], result[2]
                    next_state = np.reshape(result[0], [1, state_size])
                    agent.append_sample(state, action_made, reward)
                    score += reward

            # print('episode: {:3d} | time: {:4d} | done: {:5d}'.format(e, time, done))
            time += 1

        entropy = agent.train_model()
        # print("episode: {:3d} | score: {:3d} | entropy: {:.3f}".format(time, score, entropy))
        scores.append(score)
        episodes.append(e)
        agent.model.save_weights('save_model/model', save_format='tf')
        time_taken.append(time)
        sim.save_simulation('211220_05_train')
        print(e, sim.error)
        # sim.save_simulation('211214_{:2d}'.format(e))

    # plt.plot(episodes, time_taken, 'yellow', label='time taken')
    plt.plot(episodes, scores, 'red', label='cost')
    plt.show()
