from novels import Novel,StoryNode
import pickle

if __name__ == "__main__":
    env = Novel()
    epochs = 5
    e = 1
    while e <= epochs:
        env._reset()
        done = False
        while not done:
            action = env.action_space.sample()
            observation, reward, done, info = env._step(action)
            if done:
                print("Episode finished after {} timesteps".format(e))
                e += 1
                print("-"*20)
                print(observation)
                print("-"*20)
                print("reward is" + str(reward))
                break
