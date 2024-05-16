class BasePolicy(object):
    def __init__(self, host_agent, config):

        self.host_agent = host_agent
        self.config = config

    def step(self, obs, goal):
        pass

