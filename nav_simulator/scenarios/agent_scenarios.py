import numpy as np
import importlib

from nav_simulator.agent import Agent
from nav_simulator.utils.utils import str_to_class
def pairwise_swap_scenario(state_config, config):
    sensors = []
    for state in state_config.STATES_IN_OBS:
        if 'sensor_name' in state_config.STATE_INFO_DICT[state]:
            module_name = 'nav_simulator.sensors.' + state_config.STATE_INFO_DICT[state]['module_name']
            class_name = state_config.STATE_INFO_DICT[state]['sensor_name']
            sensors.append(str_to_class(module_name, class_name))
    sensors = list(dict.fromkeys(sensors))

    agents = []
    for ag_id in range(1):
        package_name = 'nav_simulator'
        policy_name = 'feed_through_policy'
        dynamics_name = 'pt_mass_w_heading_2o_dynamics'

        module_path = f"{package_name}.{'policies'}.{policy_name}"
        module = importlib.import_module(module_path)
        policy = getattr(module, 'FeedthroughPolicy')

        policy_name = 'feed_through_policy'
        module_path = f"{package_name}.{'dynamics'}.{dynamics_name}"
        module = importlib.import_module(module_path)
        dynamics_model = getattr(module, 'PtMassWithHeading2OrderDynamics')

        agents.append(Agent(sensors, policy, dynamics_model, state_config, config))

    return agents

