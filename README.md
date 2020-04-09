# Navigation RL

### 1. Introduction
This project trains an agent to navigate and collect banana in a continuous square environment. The environment is based on the [Unity Machine Learning Agents Toolkit](https://github.com/Unity-Technologies/ml-agents). 


A reward of +1 is provided for collecting a yellow banana, and a reward of -1 is provided for collecting a blue banana.  Thus, the agent must collect as many as yellow bananas as possible while avoiding blue bananas.  

The state space has 37 dimensions and contains the agent's velocity, along with ray-based perception of objects around agent's forward direction.  Given this information, the agent has to learn how to best select actions.  Four discrete actions are available, corresponding to:

- **`0`** - move forward.
- **`1`** - move backward.
- **`2`** - turn left.
- **`3`** - turn right.

The task is episodic, and in order to solve the environment, the agent must get an average score of +13 over 100 consecutive episodes.

![Trained Agent][trained-agent]

### 2. Getting Starting

1. Download the environment from one of the links below.  You need only select the environment that matches your operating system:
    - Linux: [click here](https://s3-us-west-1.amazonaws.com/udacity-drlnd/P1/Banana/Banana_Linux.zip)
    - Mac OSX: [click here](https://s3-us-west-1.amazonaws.com/udacity-drlnd/P1/Banana/Banana.app.zip)
    - Windows (32-bit): [click here](https://s3-us-west-1.amazonaws.com/udacity-drlnd/P1/Banana/Banana_Windows_x86.zip)
    - Windows (64-bit): [click here](https://s3-us-west-1.amazonaws.com/udacity-drlnd/P1/Banana/Banana_Windows_x86_64.zip)
    
    (_For Windows users_) Check out [this link](https://support.microsoft.com/en-us/help/827218/how-to-determine-whether-a-computer-is-running-a-32-bit-version-or-64) if you need help with determining if your computer is running a 32-bit version or 64-bit version of the Windows operating system.

2. Place the **unzip** file in the `env` directory 

### 3. Requirements

This project requires **Python 3.6** and for the libraries check the `requirements.txt` file. In short, the required libraries are:

- [NumPy](http://www.numpy.org/)
- [Matplotlib](https://matplotlib.org/)
- [Torch](https://pytorch.org)
- [UnityAgents](https://github.com/Unity-Technologies/ml-agents)
- [OpenAI Gym](https://gym.openai.com)

### 4. Approach

The proposed solution relies on Deep Q-learning (DQN) [1] and Double DQN (DDQN) [2] algorithms to solve the task.

![DQN Score][dqn-score]

![DDQN Score][ddqn-score]

### 5. References

[1] V. Mnih, K. Kavukcuoglu, D. Silver, A. A. Rusu, J. Veness, M. G. Bellemare, A. Graves, M. Riedmiller, A. K. Fidjeland, G. Ostrovski, S. Petersen, C. Beat- tie, A. Sadik, I. Antonoglou, H. King, D. Kumaran, D. Wierstra, S. Legg, and D. Hassabis, "[Human-level control through deep reinforcement learning](https://web.stanford.edu/class/psych209/Readings/MnihEtAlHassibis15NatureControlDeepRL.pdf),” Nature, vol. 518, no. 7540, pp. 529–533, Feb 2015.

[2] H. Van Hasselt, A. Guez, and D. Silver, "[Deep reinforcement learning with double q-learning](https://www.aaai.org/ocs/index.php/AAAI/AAAI16/paper/download/12389/11847)," in Thirtieth AAAI Conference on Artificial Intelligence, 2016.

[//]: # (Image References)

[trained-agent]: https://user-images.githubusercontent.com/10624937/42135619-d90f2f28-7d12-11e8-8823-82b970a54d7e.gif "Trained Agent"

[dqn-score]: report/figures/dqn_score.pdf
[ddqn-score]: report/figures/ddqn_score.pdf

