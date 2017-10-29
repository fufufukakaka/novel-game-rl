from novels import Novel,StoryNode
from gym import wrappers
import numpy as np
import pickle
import matplotlib.pyplot as plt
from tqdm import tqdm

if __name__ == "__main__":
    env = Novel()
    # env = wrappers.Monitor(env, 'result/experiment',force=True)

    Q = np.zeros([env.observation_space.n,env.action_space.n])

    lr = 0.7 #learning rate
    disct= 0.99 #discount rate

    history = []

    epochs = 100000
    e = 1
    for i in tqdm(range(epochs)):
        observation_0 = env._reset()
        done = False
        reward = 0
        while not done:
            #observation before action
            a = np.argmax(Q[observation_0,:] + np.random.randn(1,env.action_space.n)*(1.0/(e+1)))

            action = env.action_space.sample()
            observation_1, reward, done, info = env._step(action)

            Q[observation_0,a] = (1-lr) * Q[observation_0,a] + lr * (reward + disct * np.max(Q[observation_1,:]))

            observation_0 = observation_1

            if done:
                # print("Episode finished after {} timesteps".format(e))
                e += 1
                history.append(reward)
    plt.plot(history)
    plt.show()
