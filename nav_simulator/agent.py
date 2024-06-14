import numpy as np
from nav_simulator.utils.end_conditions import _check_if_at_goal
from copy import copy

class Agent(object):
    def __init__(self,
                 id,
                 initial_pos,
                 initial_heading,
                 initial_vel,
                 initial_angular_vel,
                 goal,
                 radius,
                 sensors,
                 policy,
                 dynamics_model,
                 state_config,
                 env_config):

        self.state_config = state_config
        self.env_config = env_config



        self.radius = radius
        self.id = id
        if self.id==0:
            self.type = 'robot'
        else:
            self.type = 'pedestrian'
        self.t = 0

        self.pos_global_frame = initial_pos
        self.heading_global_frame = initial_heading[0]
        self.goal_global_frame = goal

        goal_direction = self.goal_global_frame - self.pos_global_frame / np.linalg.norm(self.goal_global_frame - self.pos_global_frame) +0.001

  
        self.vel_global_frame = initial_vel
        self.angular_speed_global_frame = initial_angular_vel[0]

        self.near_goal_threshold = env_config['near_goal_threshold']

        # get sensors

        self.sensors = [sensor(env_config) for sensor in sensors]

        self.end_condition = [_check_if_at_goal]
        self.is_at_goal = False
        self.in_collision_with_pedestrian = False
        self.in_collision_with_robot = False
        self.done = False

        self.policy = policy(host_agent=self, env_config=self.env_config)
        self.dynamics_model = dynamics_model(host_agent=self, env_config=self.env_config)

        self.min_distances_to_obstacles = 1000 * np.ones(10)
        self.distances_to_obstacles = self.min_distances_to_obstacles
        self.travelled_dist = 0.0
        self.straight_line_dist = np.linalg.norm(self.goal_global_frame - self.pos_global_frame) - self.env_config['near_goal_threshold']

    def step(self, outside_action, obs=None):
        action = self.policy.step(outside_action, obs)
        self.prevoius_pos = copy(self.pos_global_frame)
        self._take_action(action)

        # compute distances to obstacles

        for i in range(len(obs)):
            if i != self.id:
                pos_other = obs[i].pos_global_frame
                self.distances_to_obstacles[i] = np.linalg.norm(self.prevoius_pos - pos_other)

        self.min_distances_to_obstacles = np.minimum(self.min_distances_to_obstacles, self.distances_to_obstacles)

        if not self.done:
            self.t += 1
            self.travelled_dist += np.linalg.norm(self.pos_global_frame - self.prevoius_pos)

        self._check_end_condition(obs)



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
        self.dynamics_model.step(action)
        # if not self.is_at_goal:
        #     self.dynamics_model.step(action)
        # else:
        #     self.vel_global_frame = np.array([0.0, 0.0])
        #     self.angular_speed_global_frame = 0.0
        #     self.speed_global_frame = 0.0


    def _check_end_condition(self, obs):
        for end_condition in self.end_condition:
            end_condition(self, obs= obs)

