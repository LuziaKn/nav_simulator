import numpy as np
import gymnasium as gym
from nav_simulator.policies.base_policy import BasePolicy

class FeedthroughPolicy(BasePolicy):
    def __init__(self, host_agent, config):
        super(FeedthroughPolicy, self).__init__(host_agent, config)

    def step(self, action) -> np.ndarray:
        return action

    def reset(self):
        pass