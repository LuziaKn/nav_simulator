from nav_simulator.evaluation.utils.saving import save_stats_txt
import os
class Evaluator():
    def __init__(self, save_dir, exp_id,  dt):
        self.times_to_goal = []
        self.min_distance = []
        self.dt = dt
        self.save_dir = save_dir
        self.exp_id = exp_id

        if os.path.isfile(self.save_dir + f"{exp_id}_evaluation_summary.txt"):
            # Delete the file
            os.remove(self.save_dir + f"{exp_id}_evaluation_summary.txt")


    def get_data(self, agents, episode_number):
        self.times_to_goal.append([agent.t * self.dt for agent in agents])
        self.min_distance.append([min(agent.min_distances_to_obstacles) for agent in agents])

    def save_data(self, episode_number):
        save_stats_txt(self.save_dir, f"{self.exp_id}_evaluation_summary.txt", self.times_to_goal, episode_number)











