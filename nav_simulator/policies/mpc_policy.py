import pickle
from nav_simulator.policies.base_policy import BasePolicy

from harmony_mpcs.mpcPlanner import MPCPlanner
class MPCPolicy(BasePolicy):

    def __init__(self, host_agent, config):
        super(MPCPolicy, self).__init__(host_agent, config)

        self._config = config['mpc']
        self._robot_config = config['robot']
        self._ped_config = config['pedestrians']


        self.init_planner()

    def step(self, obs, goal):
        self._planner.compute_actions()

    def init_planner(self):

        self.solver_dir = self.config['BASE_DIR'] + '/solvers/'

        self._planner = MPCPlanner(solverDir=self.solver_dir,
                                   solverName=self.config['SOLVER_NAME'],
                                   config=self._config,
                                   robot_config=self._robot_config,
                                   ped_config=self._ped_config)
        self._planner.reset()


