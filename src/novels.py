import gym
import gym.spaces
import numpy as np
import pickle

class StoryNode:
    def __init__(self, text, actions, links):
        self.text = text # text is what shown to player
        self.actions = actions # actions are what shown to player
        self.links = links # links are internal links direct to next node.tag

# novel game environment
class Novel(gym.Env):
    def __init__(self, storyFile = "src/static/savingjohn.pickle"):
        self.storyPlot = {}
        self.startTiddler = ""
        with open(storyFile, "rb") as infile:
            self.storyPlot, self.startTiddler = pickle.load(infile,encoding='latin1')

        self.storyNode = None
        #for gym
        self.action_space = gym.spaces.Discrete(4) # action space depends on novel state
        self.observation = "" # observation. In this env, observation space is text content.
        self._reset()

    def _reset(self):
        self.tiddler = self.startTiddler
        self.storyNode = self.storyPlot[self.tiddler]
        self.observation = self.storyNode.text #initial state
        self.params_path = ""
        self.done = False

    def AssignReward(self,ending, story):
        if story.lower() == "savingjohn":
            if ending.startswith("Submerged under water once more, I lose all focus."):
                return(-10)
            if ending.startswith("Honest to God, I don't know what I see in her."):
                return(10)
            if ending.startswith("Suddenly I can see the sky."):
                return(20)
            if ending.startswith("Suspicion fills my heart and I scream."):
                return(-20)
            if ending.startswith("Even now, she's there for me."):
                return(0)
        return (0)

    #step environment
    def _step(self, action):
        #check the action in the possible action spaces
        #if not, return now state.
        possible_actions = self.get_possible_actions(self.storyNode,self.params_path)
        retry = False
        if len(possible_actions) == 0:
            self.done = True
        if action in possible_actions:
            #update state
            self.tiddler = self.storyNode.links[action]
            self.storyNode = self.storyPlot[self.tiddler]
            self.observation = self.storyNode.text #next state
        else:
            retry = True

        if self.tiddler == "Adam1.6": self.params_path = "Adam"
        elif self.tiddler == "Sam10": self.params_path = "Sam"
        elif self.tiddler == "Lucretia10": self.params_path = "Lucretia"
        elif self.tiddler == "Cherie7": self.params_path = "Cherie"
        elif self.tiddler == "Adam8": self.params_path = "Adam"
        elif self.tiddler == "Sam9": self.params_path = "Cherie"
        elif self.tiddler == "Lucretia7": self.params_path = "Cherie"

        reward = self.AssignReward(self.storyNode.text,"savingjohn")

        return self.observation, reward, self.done, {"observation": self.observation,"action":action,"retry":retry}

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
