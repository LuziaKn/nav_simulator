import numpy as np
from nav_simulator.utils.end_conditions import _check_if_at_goal

class Agent(object):
    def __init__(self,
                 id,
                 initial_pos,
                 initial_heading,
                 initial_vel,
                 initial_angular_vel,
                 goal,
                 sensors,
                 policy,
                 dynamics_model,
                 state_config,
                 config):

        self.state_config = state_config
        self.config = config

        self.policy = policy(host_agent=self, config=self.config)
        self.dynamics_model = dynamics_model(host_agent=self, config=self.config)


        self.radius = 0.5
        self.id = id
        self.t = 0

        self.pos_global_frame = initial_pos
        self.heading_global_frame = initial_heading[0]
        self.goal_global_frame = goal
        self.vel_global_frame = initial_vel
        self.angular_speed_global_frame = initial_angular_vel[0]

        self.near_goal_threshold = 0.5

        # get sensors

        self.sensors = [sensor() for sensor in sensors]

        self.end_condition = _check_if_at_goal
        self.is_at_goal = False

    def step(self, action):
        latent_action = self.policy.step(action)
        self._take_action(latent_action)

    def sense(self, agents):
        self.sensor_data = {}

        for sensor in self.sensors:
            sensor_data = sensor.sense(agents, self.id)
            self.sensor_data[sensor.sensor_type] = sensor_data



    def get_observation_dict(self, agents):
        observation = {}
        for state in self.state_config.STATES_IN_OBS:
            observation[state] = self.get_observation(state)
        return observation

    def get_observation(self, state):
        info = self.state_config.STATE_INFO_DICT[state]

        if ("agent_attr" in info and "sensor_name" in info) and (
                info["agent_attr"] is not None and info["sensor_name"] is not None
        ):
            raise ValueError(
                "For observation "
                + state
                + " both agent_attr and sensor_name are specified, but only one is allowed!"
            )
        else:
            if "agent_attr" in info and info["agent_attr"] is not None:
                obs = getattr(self, info["agent_attr"])
                if obs is None:
                    raise ValueError(
                        "For observation " + state + " invalid agent_attr given."
                    )
            elif "sensor_name" in info and info["sensor_name"] is not None:
                for sensor in self.sensors:
                    if sensor.sensor_type == info["sensor_name"]:
                        obs = sensor.get_obs()
            else:
                obs = None

        return obs

    def _take_action(self, action):
        if not self.is_at_goal:
            self.dynamics_model.step(action)
        else:
            self.vel_global_frame = np.array([0.0, 0.0])
            self.angular_speed_global_frame = 0.0
            self.speed_global_frame = 0.0

    def _check_end_condition(self):
        self.end_condition()
