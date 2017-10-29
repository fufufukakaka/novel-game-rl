import numpy as np

class PQNAgents:
    def __init__(self,env):
        self.qtable = np.zeros([env.observation_space.n,env.action_space.n])
        self.learningRate = 0.7
        self.discountRate= 0.99 # discount rate
        self.epsilon = 0.01
        self.act = 0

    def get_next_action(self,env,observation_0,epoch):
        if np.random.random() < self.epsilon:
            action = env.action_space.sample()
        else:
            action = np.argmax(self.qtable[observation_0,:] + np.random.randn(1,env.action_space.n)*(1.0/(epoch+1)))
        self.act = action
        return action

    def learn(self,env,observation_0,reward,observation_1):
        self.qtable[observation_0,self.act] = (1-self.learningRate) * self.qtable[observation_0,self.act] + self.learningRate * (reward + self.discountRate * np.max(self.qtable[observation_1,:]))
