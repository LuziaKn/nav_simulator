import numpy as np
import importlib

from nav_simulator.agent import Agent
from nav_simulator.utils.utils import str_to_class, next_even_number
def pairwise_swap_scenario(state_config, config):
    sensors = []
    for state in state_config.STATES_IN_OBS:
        if 'sensor_name' in state_config.STATE_INFO_DICT[state]:
            module_name = 'nav_simulator.sensors.' + state_config.STATE_INFO_DICT[state]['module_name']
            class_name = state_config.STATE_INFO_DICT[state]['sensor_name']
            sensors.append(str_to_class(module_name, class_name))
    sensors = list(dict.fromkeys(sensors))

    agents = []

    n_agents = 2

    # get random initial states
    initial_positions = np.zeros((n_agents, 2))
    initial_headings = np.zeros((n_agents, 1))
    initial_vels = np.zeros((n_agents, 2))
    initial_angular_vels = np.zeros((n_agents, 1))
    goals = np.zeros((n_agents, 2))
    for ag_id in range(0,next_even_number(n_agents),2):
        distance = 3#np.random.uniform(2.0, 4.0)
        angle = 0 #np.random.uniform(-np.pi, np.pi)
        x0_agent_1 = distance * np.cos(angle)
        y0_agent_1 = distance * np.sin(angle)

        distance = 3#np.random.uniform(2.0, 4.0)
        angle = np.pi#np.random.uniform(-np.pi, np.pi)
        x0_agent_2 =  distance * np.cos(angle)
        y0_agent_2 =  distance * np.sin(angle)

        initial_positions[ag_id,:] = [x0_agent_1, y0_agent_1]
        initial_positions[ag_id+1,:] = [x0_agent_2, y0_agent_2]

        goal_x_1 = x0_agent_2
        goal_y_1 = y0_agent_2

        goal_x_2 = x0_agent_1
        goal_y_2 = y0_agent_1

        goals[ag_id,:] = [goal_x_1, goal_y_1]
        goals[ag_id+1,:] = [goal_x_2, goal_y_2]


    for ag_id in range(2):
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



        if ag_id == 0:
            agents.append(Agent(id= ag_id,
                                initial_pos=initial_positions[ag_id],
                                initial_heading=initial_headings[ag_id],
                                initial_vel=initial_vels[ag_id],
                                initial_angular_vel=initial_angular_vels[ag_id],
                                goal=goals[ag_id],
                                sensors=sensors,
                                policy=policy,
                                dynamics_model=dynamics_model,
                                state_config=state_config,
                                config=config))
        else:
            policy_name = 'social_forces_policy'
            module_path = f"{package_name}.{'policies'}.{policy_name}"
            module = importlib.import_module(module_path)
            policy = getattr(module, 'SocialForcesPolicy')
            agents.append(Agent(id= ag_id,
                                initial_pos=initial_positions[ag_id],
                                initial_heading=initial_headings[ag_id],
                                initial_vel=initial_vels[ag_id],
                                initial_angular_vel=initial_angular_vels[ag_id],
                                goal=goals[ag_id],
                                sensors=sensors,
                                policy=policy,
                                dynamics_model=dynamics_model,
                                state_config=state_config,
                                config=config))

    return agents

