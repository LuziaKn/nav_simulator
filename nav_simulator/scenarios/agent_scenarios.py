import numpy as np

from nav_simulator.agent import Agent
from nav_simulator.utils.utils import str_to_class
def pairwise_swap_scenario(state_config, config):
    sensors = []
    for state in state_config.STATES_IN_OBS:
        module_name = 'nav_simulator.sensors.' + state_config.STATE_INFO_DICT[state]['module_name']
        class_name = state_config.STATE_INFO_DICT[state]['sensor_name']
        sensors.append(str_to_class(module_name, class_name))
    sensors = list(dict.fromkeys(sensors))

    agents = []
    for ag_id in range(1):
        module = __import__('nav_simulator')
        dynamics_model = getattr(module.dynamics.pt_mass_w_heading_2o_dynamics, 'PtMassWithHeading2OrderDynamics')

        agents.append(Agent(sensors, dynamics_model, state_config, config))

    return agents

