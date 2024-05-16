import numpy as np
from nav_simulator.utils.end_conditions import _check_if_at_goal
from nav_simulator.sensors.other_agents_states_sensor import OtherAgentsStatesSensor
from nav_simulator.dynamics.pt_mass_w_heading_2o_dynamics import PtMassWithHeading2OrderDynamics
class Agent(object):
    def __init__(self, sensors, dynamics_model, state_config, config):

        self.state_config = state_config
        self.config = config

        self.dynamics_model = dynamics_model(agent=self, dt = self.config['env']['dt'])

        self.radius = 0.5
        self.id = 0
        self.t = 0

        self.pos_global_frame = np.array([1,1], dtype="float64")
        self.heading_global_frame = 0.0
        self.goal_global_frame = np.array([5, 5], dtype="float64")
        self.vel_global_frame = np.array([0.0, 0.0], dtype="float64")
        self.angular_speed_global_frame = 0.0

        self.near_goal_threshold = 0.5

        # get sensors

        self.sensors = [sensor() for sensor in sensors]

        self.end_condition = _check_if_at_goal
        self.is_at_goal = False

    def step(self, action):
        self._take_action(action)

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
        info = self.EnvConfig.SensorConfig.STATE_INFO_DICT[state]

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
                obs = rgetattr(self, info["agent_attr"])
                if obs is None:
                    raise ValueError(
                        "For observation " + state + " invalid agent_attr given."
                    )
            elif "sensor_name" in info and info["sensor_name"] is not None:
                if info["sensor_name"] in self.sensors:
                    kwargs = (
                        info["sensor_kwargs"]
                        if info["sensor_kwargs"] is not None
                        else dict()
                    )
                    obs = self.sensors[info["sensor_name"]].get_obs(**kwargs)
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
