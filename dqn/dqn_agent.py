import numpy as np
import random
from collections import namedtuple, deque

from dqn.model import QNetwork

import torch
import torch.nn.functional as F
import torch.optim as optim

BUFFER_SIZE = int(1e5) # replay buffer size
BATCH_SIZE = 64        # mini-batch size
GAMMA = 0.99           # discount factor
TAU = 1e-3             # soft update of target parameters
LEARNING_RATE = 5e-4   # learning rate
UPDATE_FREQUENCY = 4   # how often the network is updated

device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

class DQNAgent:
    
    """DQN agent that iteracts and learns from the environment."""
    
    def __init__(self, state_size:int, action_size:int, seed:int):
        """Initiliaze a DQNAgent object.
        
        Args:
          state_size (int): dimension of each state
          action_size (int): dimension of each action
          seed (int):  random seed for reproductibility purpose
        """
       
        self.state_size  = state_size
        self.action_size = action_size
        self.seed = random.seed(seed)
        
        # Q-Networks
        self.qnetwork_local  = QNetwork(state_size, action_size, seed).to(device)
        self.qnetwork_target = QNetwork(state_size, action_size, seed).to(device)
        
        # Optimizer
        self.optimizer       = optim.Adam(self.qnetwork_local.parameters(), lr=LEARNING_RATE)
        
        # Replay memory
        self.memory = ReplayBuffer(action_size, BUFFER_SIZE, BATCH_SIZE, seed)
        
        # Initialize the time step (for every UPDATE_FREQUENCY steps)
        self.t_step = 0
    
    def step(self, state, action, reward, next_state, done):
        
        # Stores the experience in the replay memory
        self.memory.add(state, action, reward, next_state, done)
        
        # Learns every UPDATE_FREQUENCY time steps
        self.t_step = (self.t_step + 1) % UPDATE_FREQUENCY
        
        if self.t_step == 0:
            # if there are enough samples available in the replay memory, than, picks a random sample and learns
            if len(self.memory) > BATCH_SIZE:
                experiences = self.memory.sample()
                self.learn(experiences, GAMMA)

    def act(self, state, epsilon=0.):
        """Returns the actions for a given state according to the current performance policy.
        
        Args:
          state (array_like): current state
          epsilon (float): epsilon, for epsilon-greed action selection
        """
        
        state = torch.from_numpy(state).float().unsqueeze(0).to(device)
        self.qnetwork_local.eval()
        
        with torch.no_grad():
            action_values = self.qnetwork_local(state)
        self.qnetwork_local.train()
        
        # Epsilon-greedy action selection
        if random.random() > epsilon:
            return np.argmax(action_values.cpu().data.numpy())
        else:
            return random.choice(np.arange(self.action_size))
    
    def learn(self, experiences, gamma):
        
        """Update the value of the parameters using a given batch of experience tuples.
        
        Args:
          experiences: (Tuple[torch.Tensor]): tuple of (s, a, r, s', done) tuples
          gamma (float): discount factor
        """
        
        states, actions, rewards, next_states, dones = experiences
        
        # Get the max predict Q-values for the next_states from the target neural network
        Q_targets_next = self.qnetwork_target(next_states).detach().max(1)[0].unsqueeze(1)
        
        # Compute the next Q-values for the next_states
        Q_targets = rewards + (gamma * Q_targets_next * (1 - dones))
        
        # Get the expected Q-value of the current states from the local neural network
        Q_expected = self.qnetwork_local(states).gather(1, actions)
        
        # Compute the loss
        loss = F.mse_loss(Q_expected, Q_targets)
        # Minimize the loss
        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()
        
        # Updates the target network
        self.soft_update(self.qnetwork_local, self.qnetwork_target, TAU)
        
    def soft_update(self, local_model, target_model, tau):
        
        """Soft update model's parameters.
        
        θ_target = τ*θ_local + (1 - τ)*θ_target
        
        Args:
         local_model (PyTorch model): weigths to be copied from
         target_model (PyTorch model): weights to be copied to
         tau (float): interpolation parameter
        """
        
        for target_param, local_param in zip(target_model.parameters(), local_model.parameters()):
            target_param.data.copy_(tau * local_param.data + (1.0 - tau) * target_param.data)


class DDQNAgent(DQNAgent):
    
    """DDQN agent that iteracts and learns from the environment."""
    
    def __init__(self, state_size, action_size, seed):
        """
           Initialize a DDQNAgent object.
           
           Args:
             state_size (int): dimension of each state
             action_size (int): dimension of each action
             seed (int): random seed for reproductibility purpose
        """
        super(DDQNAgent, self).__init__(state_size, action_size, seed)
        
        # Replay memory
        self.memory = ReplayBuffer(action_size, BUFFER_SIZE, BATCH_SIZE, seed)
        
        # Initialize the time step (for every UPDATE_FREQUENCY steps)
        self.t_step = 0
    
    def learn(self, experiences, gamma):
        
        """
          Update the values of the parameters using a given batch of experience tuples.
          
          Args:
            experiences (Tuple[torch.Tensor]): tuple of (s, a, r, s', done) tuples
            gamma (float): discount factor
        """
        
        states, actions, rewards, next_states, dones = experiences
        
        # Selects the best actions based on the next_states
        argmax_actions = self.qnetwork_local(next_states).detach().max(1)[1].unsqueeze(1)
        
        # Evaluates that best action on the target network
        Q_targets_next = self.qnetwork_target(next_states).gather(1, argmax_actions)
        
        # Compute the next Q-values for the next_states
        Q_targets = rewards + (gamma * Q_targets_next * (1 - dones))
        
        # Get the expected Q-value of the current states from the local neural network
        Q_expected = self.qnetwork_local(states).gather(1, actions)
        
        # Compute the loss
        loss = F.mse_loss(Q_expected, Q_targets)
        # Minimize the loss
        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()
        
        # soft-update the target network
        self.soft_update(self.qnetwork_local, self.qnetwork_target, TAU)

        

class ReplayBuffer:
    """Fixed-size buffer to store experience tuples."""

    def __init__(self, action_size, buffer_size, batch_size, seed):
        """Initialize a ReplayBuffer object.

        Args:
            action_size (int): dimension of each action
            buffer_size (int): maximum size of the buffer
            batch_size (int): size of each training batch
            seed (int): random seed
        """
        
        self.action_size = action_size
        self.memory = deque(maxlen=buffer_size)  
        self.batch_size = batch_size
        self.experience = namedtuple("Experience", field_names=["state", "action", "reward", "next_state", "done"])
        self.seed = random.seed(seed)
    
    def add(self, state, action, reward, next_state, done):
        """Add a new experience to memory."""
        
        e = self.experience(state, action, reward, next_state, done)
        self.memory.append(e)
    
    def sample(self):
        """Randomly sample a batch of experiences from memory."""
        
        experiences = random.sample(self.memory, k=self.batch_size)

        states = torch.from_numpy(np.vstack([e.state for e in experiences if e is not None])).float().to(device)
        actions = torch.from_numpy(np.vstack([e.action for e in experiences if e is not None])).long().to(device)
        rewards = torch.from_numpy(np.vstack([e.reward for e in experiences if e is not None])).float().to(device)
        next_states = torch.from_numpy(np.vstack([e.next_state for e in experiences if e is not None])).float().to(device)
        dones = torch.from_numpy(np.vstack([e.done for e in experiences if e is not None]).astype(np.uint8)).float().to(device)
  
        return (states, actions, rewards, next_states, dones)

    def __len__(self):
        """Return the current size of internal memory."""
        return len(self.memory)
        
        
        
        
        
        
        
        
        
        
        
    