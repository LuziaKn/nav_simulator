import numpy as np

from nav_simulator.agent import Agent
from nav_simulator.utils.utils import str_to_class
def pairwise_swap_scenario(config):
    sensors = []
    for state in config.STATES_IN_OBS:
        module_name = 'nav_simulator.sensors.' + config.STATE_INFO_DICT[state]['module_name']
        class_name = config.STATE_INFO_DICT[state]['sensor_name']
        sensors.append(str_to_class(module_name, class_name))
    sensors = list(dict.fromkeys(sensors))

    agents = []
    for ag_id in range(1):
        agents.append(Agent(sensors, config))

    return agents

