import numpy as np

class StateConfig(object):
    def __init__(self):
        self.MAX_NUM_OTHER_AGENTS_OBSERVED = 2 #todo

        self.STATES_IN_OBS = ["other_agents_states",
                               "pos_global_frame",
                                 "heading_global_frame",
                                   "vel_global_frame",
                                     "angular_speed_global_frame",
                                       "goal_global_frame",
                                         "other_agents_params"]

        self.STATE_INFO_DICT = {
            'other_agents_states': {
                'dtype': np.float32,
                'size': (self.MAX_NUM_OTHER_AGENTS_OBSERVED,6),
                'bounds': [-np.inf, np.inf],
                "sensor_name": "OtherAgentsStatesSensor",
                "module_name": 'other_agents_states_sensor',
                'attr': 'get_sensor_data("other_agents_states")',
                'std': np.tile(np.array([5.0, 5.0, 1.0, 1.0, 1.0, 5.0, 1.0], dtype=np.float32), (self.MAX_NUM_OTHER_AGENTS_OBSERVED, 1)),
                'mean': np.tile(np.array([0.0, 0.0, 0.0, 0.0, 0.5, 0.0, 1.0], dtype=np.float32), (self.MAX_NUM_OTHER_AGENTS_OBSERVED, 1)),
                },
            'other_agents_params': {
                'dtype': np.float32,
                'size': (self.MAX_NUM_OTHER_AGENTS_OBSERVED,2),
                'bounds': [-np.inf, np.inf],
                "sensor_name": "OtherAgentsParamsSensor",
                "module_name": 'other_agents_params_sensor',
                'attr': 'get_sensor_data("other_agents_params")',
                'std': np.tile(np.array([5.0, 5.0, ], dtype=np.float32), (self.MAX_NUM_OTHER_AGENTS_OBSERVED, 1)),
                'mean': np.tile(np.array([0.0, 0.0], dtype=np.float32), (self.MAX_NUM_OTHER_AGENTS_OBSERVED, 1)),
                },
            "pos_global_frame": {
                "dtype": np.float64,
                "size": 2,
                "bounds": [-np.inf, np.inf],
                "agent_attr": "pos_global_frame",
            },
            "vel_global_frame": {
                "dtype": np.float64,
                "size": 2,
                "bounds": [-np.inf, np.inf],
                "agent_attr": "vel_global_frame",
            },
            "heading_global_frame": {
                "dtype": np.float64,
                "size": 1,
                "bounds": [-np.pi, np.pi],
                "agent_attr": "heading_global_frame",
            },
            "angular_speed_global_frame": {
                "dtype": np.float64,
                "size": 1,
                "bounds": [-np.pi, np.pi],
                "agent_attr": "angular_speed_global_frame",
            },
            "goal_global_frame": {
                "dtype": np.float64,
                "size": 2,
                "bounds": [-np.inf, np.inf],
                "agent_attr": "goal_global_frame",
            },
        }