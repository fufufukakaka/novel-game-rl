import gym
import gym.spaces
import pickle

class StoryNode:
    def __init__(self, text, actions, links):
        self.text = text # text is what shown to player
        self.actions = actions # actions are what shown to player
        self.links = links # links are internal links direct to next node.tag

# novel game environment
class NovelSavingJohn(gym.Env):
    def __init__(self, storyFile = "src/static/savingjohn.pickle"):
        self.storyPlot = {}
        self.startTiddler = ""
        with open(storyFile, "rb") as infile:
            self.storyPlot, self.startTiddler = pickle.load(infile,encoding='latin1')

        t = 0
        self.plotNumber = {}
        for i in list(self.storyPlot.keys()):
            self.plotNumber[i] = t
            t += 1

        self.storyNode = None
        # for gym
        self.action_space = gym.spaces.Discrete(5) # action space depends on novel state
        self.observation_space = gym.spaces.Discrete(t)
        self.observation = "" # In this env, observation space is text content or discrete number.

    def _reset(self,number):
        self.tiddler = self.startTiddler
        self.storyNode = self.storyPlot[self.tiddler]
        if number:
            self.observation = self.plotNumber[self.tiddler] #for plain q-learning
        else:
            self.observation = self.storyNode.text #initial state
        self.params_path = ""
        self.done = False
        return self.observation

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
    def _step(self, action,number):
        # check the action in the possible action spaces
        # if not, return now state.
        possible_actions = self.get_possible_actions(self.storyNode,self.params_path)
        retry = False
        if len(possible_actions) == 0:
            self.done = True
        if action in possible_actions:
            # print(self.storyNode.actions[action])
            # update state
            self.tiddler = self.storyNode.links[action]
            self.storyNode = self.storyPlot[self.tiddler]
            if number:
                self.observation = self.plotNumber[self.tiddler]
            else:
                self.observation = self.storyNode.text #next state
            #
            # print(self.storyNode.text)
        else:
            retry = True
            # print("retry")

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
            if params_path == "Adam": actions.append(1)
            elif params_path == "Sam": actions.append(2)
            elif params_path == "Lucretia": actions.append(3)
            elif params_path == "Cherie": actions.append(4)
        else:
            for i in range(len(storyNode.actions)):
                actions.append(i)
        return actions

class NovelMachineOfDeath(gym.Env):
    def __init__(self):
        self.title = "MachineOfDeath"
        self.methodDict = {}
        self.methodDict["Cut off"] = self.tiddler0
        self.methodDict["Sarah"] = self.tiddler1
        self.methodDict["There's a light"] = self.tiddler2
        self.methodDict["Nights"] = self.tiddler164
        self.methodDict["Explain"] = self.tiddler4
        self.methodDict["Holy crap, I can't believe that worked"] = self.tiddler110
        self.methodDict["Your goose is cooked!"] = self.tiddler6
        self.methodDict["Leap"] = self.tiddler7
        self.methodDict["Suicide"] = self.tiddler98
        self.methodDict["Look out below"] = self.tiddler9
        self.methodDict["Keep running"] = self.tiddler137
        self.methodDict["Wigs"] = self.tiddler11
        self.methodDict["Not over until the chiselled rocker sings"] = self.tiddler43
        self.methodDict["Untitled Passage 2"] = self.tiddler15
        self.methodDict["No"] = self.tiddler100
        self.methodDict["Watch"] = self.tiddler16
        self.methodDict["SHOT THROUGH THE HEART BY BON JOVI"] = self.tiddler17
        self.methodDict["Knock, knock!"] = self.tiddler18
        self.methodDict["Tackle"] = self.tiddler19
        self.methodDict["StoryTitle"] = self.tiddler20
        self.methodDict["Wait"] = self.tiddler21
        self.methodDict["Shoot"] = self.tiddler22
        self.methodDict["Whew!"] = self.tiddler135
        self.methodDict["Bar"] = self.tiddler23
        self.methodDict["Eating a sinner"] = self.tiddler24
        self.methodDict["LOOKING UP NOTES"] = self.tiddler25
        self.methodDict["Gone home"] = self.tiddler26
        self.methodDict["Leave"] = self.tiddler28
        self.methodDict["Blood"] = self.tiddler172
        self.methodDict["Up your alley"] = self.tiddler29
        self.methodDict["Couldn't have known"] = self.tiddler30
        self.methodDict["That song was terrible"] = self.tiddler31
        self.methodDict["Yell"] = self.tiddler32
        self.methodDict["He drinks"] = self.tiddler33
        self.methodDict["TODO"] = self.tiddler34
        self.methodDict["Waiting together"] = self.tiddler35
        self.methodDict["Sinner"] = self.tiddler36
        self.methodDict["Outside the karaoke bar"] = self.tiddler37
        self.methodDict["Unjabbed"] = self.tiddler195
        self.methodDict["Eat eat eat"] = self.tiddler38
        self.methodDict["The hard truth"] = self.tiddler40
        self.methodDict["Gotta go fast!"] = self.tiddler41
        self.methodDict["Nothing to hide"] = self.tiddler130
        self.methodDict["Play to win"] = self.tiddler44
        self.methodDict["Did you forget he's not real?"] = self.tiddler45
        self.methodDict["Gunless"] = self.tiddler46
        self.methodDict["From my cold, dead hands"] = self.tiddler47
        self.methodDict["Blonde"] = self.tiddler48
        self.methodDict["Kitchen"] = self.tiddler76
        self.methodDict["Inside car"] = self.tiddler49
        self.methodDict["Shoo"] = self.tiddler51
        self.methodDict["Quit"] = self.tiddler52
        self.methodDict["Lister"] = self.tiddler53
        self.methodDict["Excused"] = self.tiddler54
        self.methodDict["Reveal"] = self.tiddler55
        self.methodDict["Bedroom drawers"] = self.tiddler56
        self.methodDict["Standing your ground"] = self.tiddler57
        self.methodDict["Axe to grind"] = self.tiddler58
        self.methodDict["AB"] = self.tiddler177
        self.methodDict["In da house"] = self.tiddler59
        self.methodDict["Sit on it"] = self.tiddler193
        self.methodDict["Drink up"] = self.tiddler60
        self.methodDict["The choice"] = self.tiddler61
        self.methodDict["See no evil"] = self.tiddler62
        self.methodDict["Losing smile"] = self.tiddler63
        self.methodDict["Rescue"] = self.tiddler64
        self.methodDict["So clean"] = self.tiddler65
        self.methodDict["Eating a floater"] = self.tiddler66
        self.methodDict["Eating a lister"] = self.tiddler67
        self.methodDict["Explore"] = self.tiddler68
        self.methodDict["Wake"] = self.tiddler69
        self.methodDict["One on one"] = self.tiddler70
        self.methodDict["On the beach"] = self.tiddler50
        self.methodDict["Goose!"] = self.tiddler72
        self.methodDict["A message"] = self.tiddler73
        self.methodDict["Stairs"] = self.tiddler74
        self.methodDict["Splat"] = self.tiddler75
        self.methodDict["Thanks"] = self.tiddler27
        self.methodDict["A slip of paper"] = self.tiddler77
        self.methodDict["Sir"] = self.tiddler151
        self.methodDict["David"] = self.tiddler79
        self.methodDict["OLD AGE NOTES"] = self.tiddler80
        self.methodDict["The meeting"] = self.tiddler81
        self.methodDict["Hell cab"] = self.tiddler82
        self.methodDict["Ignition"] = self.tiddler83
        self.methodDict["Axe"] = self.tiddler84
        self.methodDict["Butt"] = self.tiddler71
        self.methodDict["Ignore"] = self.tiddler85
        self.methodDict["Run, run"] = self.tiddler86
        self.methodDict["Standing in a mall"] = self.tiddler87
        self.methodDict["Photo"] = self.tiddler39
        self.methodDict["Meeting 1"] = self.tiddler89
        self.methodDict["LOOKING UP"] = self.tiddler90
        self.methodDict["OLD AGE"] = self.tiddler91
        self.methodDict["Snatched"] = self.tiddler92
        self.methodDict["Bedroom"] = self.tiddler93
        self.methodDict["StoryAuthor"] = self.tiddler94
        self.methodDict["Yes"] = self.tiddler95
        self.methodDict["You first"] = self.tiddler96
        self.methodDict["Brunette"] = self.tiddler188
        self.methodDict["SWERVE"] = self.tiddler97
        self.methodDict["Death"] = self.tiddler8
        self.methodDict["Closet"] = self.tiddler14
        self.methodDict["No thanks"] = self.tiddler78
        self.methodDict["BON JOVI NOTES"] = self.tiddler101
        self.methodDict["Teeth"] = self.tiddler103
        self.methodDict["Poison"] = self.tiddler104
        self.methodDict["Start"] = self.tiddler105
        self.methodDict["Returns"] = self.tiddler106
        self.methodDict["Exit"] = self.tiddler107
        self.methodDict["Meeting"] = self.tiddler108
        self.methodDict["Doggy with a gun"] = self.tiddler109
        self.methodDict["Cupboard"] = self.tiddler111
        self.methodDict["Dive"] = self.tiddler112
        self.methodDict["Killing time"] = self.tiddler152
        self.methodDict["Rank"] = self.tiddler114
        self.methodDict["Phone"] = self.tiddler115
        self.methodDict["Making a stool of yourself"] = self.tiddler116
        self.methodDict["UFO Catcher"] = self.tiddler117
        self.methodDict["Floater"] = self.tiddler118
        self.methodDict["Ain't worth it"] = self.tiddler119
        self.methodDict["Rumbly tummy"] = self.tiddler120
        self.methodDict["Diarroiah"] = self.tiddler121
        self.methodDict["Eating an A.B."] = self.tiddler155
        self.methodDict["Card"] = self.tiddler123
        self.methodDict["Reveal to Rachel"] = self.tiddler124
        self.methodDict["Sofahh"] = self.tiddler125
        self.methodDict["Reflection"] = self.tiddler126
        self.methodDict["Gotten me killed"] = self.tiddler127
        self.methodDict["Stealth eater"] = self.tiddler128
        self.methodDict["Time to talk"] = self.tiddler129
        self.methodDict["Gun"] = self.tiddler131
        self.methodDict["Outta here"] = self.tiddler132
        self.methodDict["The drive home"] = self.tiddler133
        self.methodDict["Busted"] = self.tiddler134
        self.methodDict["Drinking tea together"] = self.tiddler5
        self.methodDict["Waiting in the kitchen"] = self.tiddler136
        self.methodDict["Beneath"] = self.tiddler10
        self.methodDict["Logo"] = self.tiddler185
        self.methodDict["Painting"] = self.tiddler138
        self.methodDict["Uninterested"] = self.tiddler139
        self.methodDict["Something foyer"] = self.tiddler140
        self.methodDict["Crazy"] = self.tiddler141
        self.methodDict["Streets"] = self.tiddler143
        self.methodDict["BREAK"] = self.tiddler144
        self.methodDict["Meeting 2"] = self.tiddler145
        self.methodDict["Still crazy"] = self.tiddler146
        self.methodDict["Duck"] = self.tiddler147
        self.methodDict["TIME TRAVEL MISHAP"] = self.tiddler148
        self.methodDict["Sure do"] = self.tiddler149
        self.methodDict["Not this time"] = self.tiddler150
        self.methodDict["Continue meeting"] = self.tiddler88
        self.methodDict["Pee freely"] = self.tiddler113
        self.methodDict["Showtime!"] = self.tiddler153
        self.methodDict["Menu"] = self.tiddler154
        self.methodDict["Time to go"] = self.tiddler122
        self.methodDict["Dressing time"] = self.tiddler156
        self.methodDict["Looking"] = self.tiddler157
        self.methodDict["Outside"] = self.tiddler158
        self.methodDict["Calm"] = self.tiddler159
        self.methodDict["Not at all"] = self.tiddler160
        self.methodDict["Winning smile"] = self.tiddler161
        self.methodDict["Attack!"] = self.tiddler162
        self.methodDict["Sing a song"] = self.tiddler163
        self.methodDict["Her"] = self.tiddler99
        self.methodDict["Restaurant"] = self.tiddler167
        self.methodDict["Poster"] = self.tiddler165
        self.methodDict["YOU'RE A TERRIBLE PERSON"] = self.tiddler166
        self.methodDict["Dress to impress"] = self.tiddler3
        self.methodDict["Photos"] = self.tiddler169
        self.methodDict["Meaning"] = self.tiddler170
        self.methodDict["Dismantle and dispose"] = self.tiddler171
        self.methodDict["Knocked his block off!"] = self.tiddler168
        self.methodDict["Drive off"] = self.tiddler173
        self.methodDict["Ask"] = self.tiddler174
        self.methodDict["A cold kitchen"] = self.tiddler175
        self.methodDict["Why"] = self.tiddler176
        self.methodDict["Your move!"] = self.tiddler12
        self.methodDict["Lost"] = self.tiddler178
        self.methodDict["Later"] = self.tiddler179
        self.methodDict["No pee for me!"] = self.tiddler180
        self.methodDict["Drawers"] = self.tiddler181
        self.methodDict["Gun grab"] = self.tiddler182
        self.methodDict["The Machine"] = self.tiddler183
        self.methodDict["Co-workers"] = self.tiddler184
        self.methodDict["Table"] = self.tiddler142
        self.methodDict["Drink tea"] = self.tiddler186
        self.methodDict["Why the dive?"] = self.tiddler187
        self.methodDict["Wrestle"] = self.tiddler42
        self.methodDict["Life after Sarah"] = self.tiddler189
        self.methodDict["Fuck"] = self.tiddler190
        self.methodDict["Pantry"] = self.tiddler191
        self.methodDict["Another"] = self.tiddler192
        self.methodDict["The beginning"] = self.tiddler102
        self.methodDict["Yet another"] = self.tiddler194
        self.methodDict["What a rotten way to die"] = self.tiddler13
        self.methodDict["Sloppy eater"] = self.tiddler196
        self.methodDict["Leave meeting"] = self.tiddler197
        self.methodDict["Floordrobe"] = self.tiddler198
        self.methodDict["The door"] = self.tiddler199

        self.doShuffle = False
        self.myHTMLParser = MyHTMLParser()
        self.doParaphrase = False
        # for gym
        self.action_space = gym.spaces.Discrete(5) # action space depends on novel state
        self.observation_space = gym.spaces.Discrete(t)
        self.observation = "" # In this env, observation space is text content or discrete number.

        self. _reset()

    def _reset(self,number):
        self.current_tiddler = "Start"
        self.params = defaultdict(int)
        self.observation = self.methodDict[self.current_tiddler] #initial state
        self.done = False
        return self.observation

    def AssignReward(self,ending, story):
        if story.lower() == "machineofdeath":
            if not """THE END""" in ending:
                return(-0.1)
            if """You spend your last few moments on Earth lying there, shot through the heart, by the image of Jon Bon Jovi.""" in ending:
                return(-20)
            if """You may be locked away for some time.""" in ending:
                return(-10)
            if """Eventually you're escorted into the back of a police car as Rachel looks on in horror.""" in ending:
                return(-10)
            if """You can't help but smile.""" in ending:
                return(20)
            if """Fate can wait.""" in ending:
                return(-10)
            if """you hear Bon Jovi say as the world fades around you.""" in ending:
                return(-20)
            if """Hope you have a good life.""" in ending:
                return(20)
            if """As the screams you hear around you slowly fade and your vision begins to blur, you look at the words which ended your life.""" in ending:
                return(-20)
            if """Sadly, you're so distracted with looking up the number that you don't notice the large truck speeding down the street.""" in ending:
                return(-10)
            if """Stay the hell away from me!&quot; she blurts as she disappears into the crowd emerging from the bar.""" in ending:
                return(10)
            if """Congratulations!""" in ending:
                return(20)
            if """All these hiccups lead to one grand disaster.""" in ending:
                return(-10)
            if """After all, it's your life. It's now or never. You ain't gonna live forever. You just want to live while you're alive.""" in ending:
                return(30)
            if """Rachel waves goodbye as you begin the long drive home. After a few minutes, you turn the radio on to break the silence.""" in ending:
                return(20)
        return (0)

    #step environment
    def _step(self, action,number):
        # check the action in the possible action spaces
        # if not, return now state.
        possible_actions = self.get_possible_actions(self.storyNode,self.params_path)
        retry = False
        if len(possible_actions) == 0:
            self.done = True
        if action in possible_actions:
            # print(self.storyNode.actions[action])
            # update state
            self.tiddler = self.storyNode.links[action]
            self.storyNode = self.storyPlot[self.tiddler]
            if number:
                self.observation = self.plotNumber[self.tiddler]
            else:
                self.observation = self.storyNode.text #next state
            #
            # print(self.storyNode.text)
        else:
            retry = True
            # print("retry")

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
            if params_path == "Adam": actions.append(1)
            elif params_path == "Sam": actions.append(2)
            elif params_path == "Lucretia": actions.append(3)
            elif params_path == "Cherie": actions.append(4)
        else:
            for i in range(len(storyNode.actions)):
                actions.append(i)
        return actions
