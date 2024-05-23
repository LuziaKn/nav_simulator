import gymnasium as gym
import numpy as np
import yaml
import os
import pyglet
from pyglet.window import key
import threading

from nav_simulator.states_config import StateConfig
from nav_simulator.scenarios.agent_scenarios import pairwise_swap_scenario
from nav_simulator.utils.utils import str_to_class
from nav_simulator.visualization.matplotlib_visualizer import Visualizer
from nav_simulator.visualization.mpc_visualizer import MPCVisualizer

class Nav2DEnv(gym.Env):
    def __init__(self, config_dir=None):

        super(Nav2DEnv, self).__init__()

        self.StateConfig = StateConfig()

        if config_dir == None:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            config_dir = current_dir + '/config/'

        with open(config_dir + 'config.yaml', 'r') as stream:
            try:
                self.config = yaml.safe_load(stream)
            except yaml.YAMLError as exc:
                print(exc)

        self.config['BASE_DIR'] = os.path.dirname(os.path.abspath(__file__))
        self.plot_save_dir = '/home/luzia/code/harmony_mpcs/results/'

        self.visualizer = MPCVisualizer(self.plot_save_dir,
                                     config = self.config,
                                     limits = [[-5,5], [-5,5]],
                                     fig_size = (10,10),
                                     save_figures = False,
                                     save_for_animation = False,
                                     save_every_n_plots = 5,
                                     keep_frames = True,
                                     replay = False,
                                     debug = False,
                                     show = True)

        self.max_num_agents = 2
        self.min_speed = -1.0
        self.max_speed = 1.0
        self.min_heading_change = -1.0
        self.max_heading_change = 1.0

        self._init_action_space()
        self._init_observation_space()

        self.episode_number = 0
        self.game_over = False

        self.agents = None

        self._plot_infos_dict = {}


        self.reward_range = (-float('inf'), float('inf'))
        self.metadata = None
        self.spec = None
        self.done = False
        self.info = None
        self.state = None


    def reset(self):

        if self.agents is not None:
            self.visualizer.init_episode_plot(self.agents)
            self.visualizer.animate_episode(n_agents=len(self.agents),
                                            episode=self.episode_number,
                                            ego_policy='mpc',
                                            ego_planning_type='fixed',
                                            others_policy='tets',
                                            was_in_collision=False, )

        self.episode_number += 1
        self.episode_step_number = 0

        self._init_scenario()

        self.visualizer.init_episode_plot(self.agents)

        self.done = False
        self.info = None
        return self._get_obs()

    def step(self, action):

        self.episode_step_number += 1

        # Take action for each agent
        for agent in self.agents:
            agent.step(action)
        new_action = False

        if self.game_over:
            raise RuntimeError('Episode has finished. Call `reset()`')

        which_agents_done, self.game_over = self._check_which_agents_are_done()

        next_observations = self._get_obs()

        self.info = None
        return next_observations, 0.0, self.game_over, self.info

    def render(self, mode='human'):

        self.visualizer.update_episode_plot(agents=self.agents,
                                     current_step=self.episode_step_number - 1,
                                     episode_number=self.episode_number,
                                     plot_infos_dict=self._plot_infos_dict)

    def close(self):
        pass

    def seed(self, seed=None):
        pass

    def configure(self, *args, **kwargs):
        pass


    def _init_action_space(self):
        self.low_action = np.array(
            [self.min_speed, self.min_speed,self.min_heading_change]
        )
        self.high_action = np.array(
            [self.max_speed, self.max_speed, self.max_heading_change]
        )
        self.action_space = gym.spaces.Box(
            self.low_action, self.high_action, dtype=np.float32
        )

    def _init_observation_space(self):
        self.observation = {}
        self.observation_space = gym.spaces.Dict({})

        for agent in range(self.max_num_agents):
            self.observation[agent] = {}
            self.observation_space.spaces[agent] = gym.spaces.Dict({})

        for state in self.StateConfig.STATES_IN_OBS:
            for agent in range(self.max_num_agents):
                self.observation[agent][state] = np.zeros(
                    (self.StateConfig.STATE_INFO_DICT[state]["size"]),
                    dtype=self.StateConfig.STATE_INFO_DICT[state]["dtype"],
                )
                self.observation_space.spaces[agent][state] = gym.spaces.Box(
                    self.StateConfig.STATE_INFO_DICT[state]["bounds"][0]
                    * np.ones((self.StateConfig.STATE_INFO_DICT[state]["size"])),
                    self.StateConfig.STATE_INFO_DICT[state]["bounds"][1]
                    * np.ones((self.StateConfig.STATE_INFO_DICT[state]["size"])),
                    dtype=self.StateConfig.STATE_INFO_DICT[state]["dtype"],
                )


    def _init_scenario(self):


        self.agents = pairwise_swap_scenario(self.StateConfig, self.config)

    def _check_which_agents_are_done(self):
        at_goal_condition = np.array([a.is_at_goal for a in self.agents])

        which_agents_done = at_goal_condition
        game_over = which_agents_done[0]

        return which_agents_done, bool(game_over)
        return which_agents_done, bool(game_over)






    def _get_obs(self):

        # Agents collect a reading from their map-based sensors
        for i, agent in enumerate(self.agents):
            agent.sense(self.agents)

        # Agents fill in their element of the multiagent observation vector
        for i, agent in enumerate(self.agents):
            self.observation[i] = agent.get_observation_dict(self.agents)

        if self.config['SINGLE_EGO_AGENT']:
            return self.observation[0]
        else:
            return self.observation


    def __del__(self):
        pass
    def __str__(self):
        return 'Nav2DEnv'
    def __repr__(self):
        pass

if __name__ == "__main__":

    env = Nav2DEnv()

    # Sample usage
    obs = env.reset()
    env.render()

    done = False
    while not done:
        # for event in pygame.event.get():
        #     if event.type == pygame.QUIT:
        #         done = True

        action = env.action_space.sample()  # Random action
        obs, reward, done, _ = env.step(action)
        env.render()
        print(f"Action: {action}, Reward: {reward}, Done: {done}")

    env.close()