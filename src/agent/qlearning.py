import numpy as np
from collections import deque

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

class DQNAgents:
    KERAS_BACKEND = 'tensorflow'
    EXPLORATION_STEPS = 1000000  # Number of steps over which the initial value of epsilon is linearly annealed to its final value
    INITIAL_EPSILON = 1.0  # Initial value of epsilon in epsilon-greedy
    FINAL_EPSILON = 0.1  # Final value of epsilon in epsilon-greedy
    INITIAL_REPLAY_SIZE = 10000  # Number of steps to populate the replay memory before training starts
    NUM_REPLAY_MEMORY = 100000  # Number of replay memory the agent uses for training
    BATCH_SIZE = 32  # Mini batch size
    TARGET_UPDATE_INTERVAL = 10000  # The frequency with which the target network is updated

    def __init__(self,env):
        self.qtable = np.zeros([env.observation_space.n,env.action_space.n])
        self.learningRate = 0.7
        self.discountRate= 0.99 # discount rate
        self.epsilon = INITIAL_EPSILON
        self.epsilon_step = (INITIAL_EPSILON - FINAL_EPSILON) / EXPLORATION_STEPS
        self.act = 0

        # Create replay memory
        self.replay_memory = deque()

        # Create q network
        self.s, self.q_values, q_network = self.build_network()
        q_network_weights = q_network.trainable_weights

        # Create target network
        self.st, self.target_q_values, target_network = self.build_network()
        target_network_weights = target_network.trainable_weights

        # Define target network update operation
        self.update_target_network = [target_network_weights[i].assign(q_network_weights[i]) for i in range(len(target_network_weights))]

        # Define loss and gradient update operation
        self.a, self.y, self.loss, self.grad_update = self.build_training_op(q_network_weights)

        self.sess = tf.InteractiveSession()
        self.saver = tf.train.Saver(q_network_weights)
        self.summary_placeholders, self.update_ops, self.summary_op = self.setup_summary()
        self.summary_writer = tf.train.SummaryWriter(SAVE_SUMMARY_PATH, self.sess.graph)

        self.sess.run(tf.initialize_all_variables())

        # Load network
        if LOAD_NETWORK:
            self.load_network()

        # Initialize target network
        self.sess.run(self.update_target_network)
