import numpy as np
import gymnasium as gym
from nav_simulator.policies.base_policy import BasePolicy
class SocialForcesPolicy(BasePolicy):
    def __init__(self, host_agent, config):
        super(SocialForcesPolicy, self).__init__(host_agent, config)

    def step(self, action=None) -> np.ndarray:
        action = np.array([0.2,0,0])
        return action

    def reset(self):
        pass