import Data_manager_V2
import Environment_V2
import random
import numpy as np
import tensorflow as tf
from tensorflow.keras.layers import Dense
from tensorflow.keras.optimizers import Adam

class REINFORCE(tf.keras.Model):
    def __init__(self):
        super(REINFORCE, self).__init__()
        self.fc1 = Dense(24, activation='relu')
        self.fc2 = Dense(24, activation='relu')
        self.fc_out = Dense(action_size, activation='softmax')      # softmax 함수는 출력의 합이 1

    def call(self, x):
        x = self.fc1(x)
        x = self.fc2(x)
        policy = self.fc_out(x)
        return policy               # 출력 = 각 행동을 할 확률

    class Agent:
        def __init__(self, state_size, action_size):
            self.state_size = state_size
            self.action_size = action_size

            self.discount_factor = 0.99
            
