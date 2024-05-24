class BasePolicy(object):
    def __init__(self, host_agent, env_config):

        self.host_agent = host_agent
        self.env_config = env_config

    def step(self, obs, goal):
        pass

