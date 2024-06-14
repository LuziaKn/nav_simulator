from nav_simulator.evaluation.utils.saving import save_stats_txt
import os
class Evaluator():
    def __init__(self, save_dir, exp_id,  dt):
        self.times_to_goal = []
        self.min_distance = []
        self.collision_ped_episodes = []
        self.collision_robot_episodes = []
        self.traveled_dists = []
        self.straight_line_dists = []
        self.dt = dt
        self.save_dir = save_dir
        self.exp_id = exp_id

        if os.path.isfile(self.save_dir + f"{exp_id}_evaluation_summary.txt"):
            # Delete the file
            os.remove(self.save_dir + f"{exp_id}_evaluation_summary.txt")


    def get_data(self, agents, episode_number):
        self.times_to_goal.append([agent.t * self.dt for agent in agents])
        self.min_distance.append([min(agent.min_distances_to_obstacles) for agent in agents])
        self.collision_ped_episodes.append(any([agent.in_collision_with_pedestrian for agent in agents[1:]]))
        self.collision_robot_episodes.append(agents[0].in_collision_with_pedestrian)
        self.traveled_dists.append([agent.travelled_dist for agent in agents])
        self.straight_line_dists = [agent.straight_line_dist for agent in agents]

    def save_data(self, episode_number):
        save_stats_txt(self.save_dir, f"{self.exp_id}_evaluation_summary.txt",
                       self.times_to_goal,
                        self.min_distance,
                        self.collision_ped_episodes,
                        self.collision_robot_episodes,
                        self.traveled_dists,
                        self.straight_line_dists,
                       episode_number)











