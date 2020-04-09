import torch
import torch.nn as nn
import torch.nn.functional as F

class QNetwork(nn.Module):
    """Actor Policy Model"""
    
    def __init__(self, state_size:int, action_size:int, seed:int, hidden_layers_units=[64, 64]):
        """Initiliaze the parameters and build the model
        
        Args:
          state_size: dimension of each state; i.e., it's size of the input layer
          action_size: dimension of each action
          seed: random seed
          fc1_units: number of nodes in the first hidden layer
          fc2_units: number of nodes in the second hiddel layer
        """
        
        super(QNetwork, self).__init__()
        
        self.seed = torch.manual_seed(seed)
        self.fc1 = nn.Linear(state_size, hidden_layers_units[0])
        self.fc2 = nn.Linear(hidden_layers_units[0], hidden_layers_units[1])
        self.fc3 = nn.Linear(hidden_layers_units[1], action_size)
        
    def forward(self, state):
        """Build a neural network that maps a state to action values"""
        
        h_relu1 = F.relu(self.fc1(state))
        h_relu2 = F.relu(self.fc2(h_relu1))
        yhat = self.fc3(h_relu2)
        return yhat