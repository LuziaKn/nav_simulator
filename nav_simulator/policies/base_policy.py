class BasePolicy(object):
    def __init__(self, host_agent, env_config):

        self.host_agent = host_agent
        self.env_config = env_config

        self._desired_speed = 1
        self._w_goal = 1
        self._w_social = 1
        self._goal = [1.0, 1.0]

    def step(self, obs, goal):
        pass

