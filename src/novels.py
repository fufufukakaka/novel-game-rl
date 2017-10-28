import gym
import gym.spaces
import numpy as np

# novel game environment
class Novel(gym.Env):
    def __init__(self, doShuffle, storyFile = "src/static/savingjohn.pickle"):
        self.storyPlot = {}
        self.startTiddler = ""
        with open(storyFile, "rb") as infile:
            self.storyPlot, self.startTiddler = pickle.load(infile,encoding='latin1')

        self.doShuffle = doShuffle # whether actions are shuffled when they are Read()
        self.idxShuffle = []

        self.storyNode = None
        #for gym
        self.action_space = (0, 1, 2, 3) # action space depends on novel state
        self.observation_space = "" # observation space. In this env, observation space is text content.
        self._reset()

    def _reset(self):
        self.tiddler = self.startTiddler
        self.storyNode = self.storyPlot[self.tiddler]
        self.observation = self.storyNode.text #initial state
        self.params_path = ""
        self.done = False

    def _step(self, action):

        return self.observation, reward, done, {"observation": self.observation}

    @staticmethod
    def get_possible_actions(storyNode,params_path):
        actions=[]
        if storyNode.text.startswith("A wet strand of hair hinders my vision and I'm back in the water."):
            if params_path == "Adam": actions.append(0)
            elif params_path == "Sam": actions.append(1)
            elif params_path == "Lucretia": actions.append(2)
            elif params_path == "Cherie": actions.append(3)
        else:
            for i in range(len(storyNode.actions)):
                actions.append(i)
        return actions
