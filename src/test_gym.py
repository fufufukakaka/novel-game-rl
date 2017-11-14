from novels import NovelSavingJohn,StoryNode
from agent.qlearning import PQNAgents
from gym import wrappers
import numpy as np
import pickle
from tqdm import tqdm

if __name__ == "__main__":
    env = NovelSavingJohn()
    env._reset(number=True)
    # env = wrappers.Monitor(env, 'result/experiment',force=True)

    agent = PQNAgents(env)
    history = []

    epochs = 100000
    e = 1
    for i in tqdm(range(epochs)):
        observation_0 = env._reset(number=True)
        done = False
        reward = 0
        action_history = []
        while not done:
            #observation before action
            action = agent.get_next_action(env,observation_0,e)
            action_history.append(action)

            observation_1, reward, done, info = env._step(action,number=True)
            agent.learn(env,observation_0,reward,observation_1)

            observation_0 = observation_1

            if done:
                # print("Episode finished after {} timesteps".format(e))
                e += 1
                history.append(reward)

    pickle.dump(history,open("result/history.pickle","wb"))
