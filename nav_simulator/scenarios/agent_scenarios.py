import numpy as np
import importlib

from nav_simulator.agent import Agent
from nav_simulator.utils.utils import str_to_class, next_even_number


def pairwise_swap_scenario(state_config, env_config):
    sensors = []
    for state in state_config.STATES_IN_OBS:
        if 'sensor_name' in state_config.STATE_INFO_DICT[state]:
            module_name = 'nav_simulator.sensors.' + state_config.STATE_INFO_DICT[state]['module_name']
            class_name = state_config.STATE_INFO_DICT[state]['sensor_name']
            sensors.append(str_to_class(module_name, class_name))
    sensors = list(dict.fromkeys(sensors))

    agents = []

    n_agents = env_config['max_num_agents']


    # get random initial states
    initial_positions = 100*np.ones((n_agents, 2))
    initial_headings = np.zeros((n_agents, 1))
    initial_vels = np.zeros((n_agents, 2))
    initial_angular_vels = np.zeros((n_agents, 1))
    goals = 100*np.ones((n_agents, 2))
    for ag_id in range(0,next_even_number(n_agents),2):

        is_valid = False
        try_id = 0
        dist_max = 3
        while not is_valid:
            distance = np.random.uniform(1, dist_max)
            angle = np.random.uniform(-np.pi, np.pi)
            x0_agent_1 = distance * np.cos(angle) + np.random.uniform(-0.5, 0.5)
            y0_agent_1 = distance * np.sin(angle) + np.random.uniform(-0.5, 0.5)
            is_valid, try_id = is_pos_valid([x0_agent_1, y0_agent_1], initial_positions, try_id)
            if try_id>10:
                dist_max = 6


        initial_positions[ag_id, :] = [x0_agent_1, y0_agent_1]

        is_valid = False
        try_id = 0
        dist_max = 3
        while not is_valid:
            distance = np.random.uniform(1, dist_max)
            x0_agent_2 = -distance * np.cos(angle) + np.random.uniform(-0.5, 0.5)
            y0_agent_2 = -distance * np.sin(angle) + np.random.uniform(-0.5, 0.5)
            is_valid, try_id = is_pos_valid([x0_agent_2, y0_agent_2], initial_positions, try_id)
            if try_id>10:
                dist_max = 6
                angle = np.random.uniform(-np.pi, np.pi)

        initial_positions[ag_id+1,:] = [x0_agent_2, y0_agent_2]

        goal_x_1 = x0_agent_2
        goal_y_1 = y0_agent_2

        goal_x_2 = x0_agent_1
        goal_y_2 = y0_agent_1

        goals[ag_id,:] = [goal_x_1, goal_y_1]
        goals[ag_id+1,:] = [goal_x_2, goal_y_2]




    # initial_positions[1] = [100, 100]
    # initial_positions[2] = [100, -100]
    # initial_positions[3] = [-100, 100]
    # goals[1] = [100, 105]
    # goals[2] = [100, -105]
    # goals[3] = [-100, 105]
    for ag_id in range(n_agents):
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
            radius = env_config['robot']['radius']
            agents.append(Agent(id= ag_id,
                                initial_pos=initial_positions[ag_id],
                                initial_heading=initial_headings[ag_id],
                                initial_vel=initial_vels[ag_id],
                                initial_angular_vel=initial_angular_vels[ag_id],
                                radius=radius,
                                goal=goals[ag_id],
                                sensors=sensors,
                                policy=policy,
                                dynamics_model=dynamics_model,
                                state_config=state_config,
                                env_config=env_config))
        else:
            radius = env_config['pedestrian']['radius']
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
                                radius=radius,
                                sensors=sensors,
                                policy=policy,
                                dynamics_model=dynamics_model,
                                state_config=state_config,
                                env_config=env_config))

    return agents

    def crossing_scenario(state_config, env_config):
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
        initial_positions = 100 * np.ones((n_agents, 2))
        initial_headings = np.zeros((n_agents, 1))
        initial_vels = np.zeros((n_agents, 2))
        initial_angular_vels = np.zeros((n_agents, 1))
        goals = 100 * np.ones((n_agents, 2))

        initial_positions[0] = [100, 100]
        initial_positions[1] = [100, -100]
        goals[0] = [100, 105]
        goals[1] = [100, -105]
        for ag_id in range(n_agents):
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
                radius = env_config['robot']['radius']
                agents.append(Agent(id=ag_id,
                                    initial_pos=initial_positions[ag_id],
                                    initial_heading=initial_headings[ag_id],
                                    initial_vel=initial_vels[ag_id],
                                    initial_angular_vel=initial_angular_vels[ag_id],
                                    radius=radius,
                                    goal=goals[ag_id],
                                    sensors=sensors,
                                    policy=policy,
                                    dynamics_model=dynamics_model,
                                    state_config=state_config,
                                    env_config=env_config))
            else:
                radius = env_config['pedestrian']['radius']
                policy_name = 'social_forces_policy'
                module_path = f"{package_name}.{'policies'}.{policy_name}"
                module = importlib.import_module(module_path)
                policy = getattr(module, 'SocialForcesPolicy')
                agents.append(Agent(id=ag_id,
                                    initial_pos=initial_positions[ag_id],
                                    initial_heading=initial_headings[ag_id],
                                    initial_vel=initial_vels[ag_id],
                                    initial_angular_vel=initial_angular_vels[ag_id],
                                    goal=goals[ag_id],
                                    radius=radius,
                                    sensors=sensors,
                                    policy=policy,
                                    dynamics_model=dynamics_model,
                                    state_config=state_config,
                                    env_config=env_config))

        return agents


def is_pos_valid(new_pos, position_list,try_id, distance=1.5):
    for pose in position_list:
        if np.linalg.norm(new_pos[:2] - pose[:2]) < distance:
            try_id +=1
            return False, try_id
    try_id = 0
    return True, try_id