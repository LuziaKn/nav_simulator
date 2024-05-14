import numpy as np

class StateConfig(object):
    def __init__(self):
        self.MAX_NUM_OTHER_AGENTS_OBSERVED = 2 #todo

        self.STATES_IN_OBS = ["other_agents_states"]

        self.STATE_INFO_DICT = {
                'other_agents_states': {
                'dtype': np.float32,
                'size': (self.MAX_NUM_OTHER_AGENTS_OBSERVED,7),
                'bounds': [-np.inf, np.inf],
                "sensor_name": "OtherAgentsStatesSensor",
                "module_name": 'other_agents_states_sensor',
                'attr': 'get_sensor_data("other_agents_states")',
                'std': np.tile(np.array([5.0, 5.0, 1.0, 1.0, 1.0, 5.0, 1.0], dtype=np.float32), (self.MAX_NUM_OTHER_AGENTS_OBSERVED, 1)),
                'mean': np.tile(np.array([0.0, 0.0, 0.0, 0.0, 0.5, 0.0, 1.0], dtype=np.float32), (self.MAX_NUM_OTHER_AGENTS_OBSERVED, 1)),
                },}