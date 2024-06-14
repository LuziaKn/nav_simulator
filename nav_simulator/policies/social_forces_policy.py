import numpy as np
import gymnasium as gym
from nav_simulator.policies.base_policy import BasePolicy
from nav_simulator.utils.utils import perpendicular
class SocialForcesPolicy(BasePolicy):
    def __init__(self, host_agent, env_config):
        super(SocialForcesPolicy, self).__init__(host_agent, env_config)

        self._ego_id = host_agent.id

        # Parameters
        self._rel_time = 0.54
        self._A = 4.5  # relative importance of position vs velocity vector
        self._lambdaImportance = 2  # speed interaction
        self._gamma = 0.35  # speed interaction
        self._n = 2  # angular interaction
        self._n_prime = 3

        self._epsilon = 0.01
        self._eps = self.env_config['pedestrian']['sfm']['eps']

        self._goal = host_agent.goal_global_frame
        self._w_social = env_config['pedestrian']['sfm']['w_social']
        self._w_goal = env_config['pedestrian']['sfm']['w_goal']
        self._desired_speed = env_config['pedestrian']['sfm']['desired_speed']

    def step(self, action=None, obs= None) -> np.ndarray:
        if obs == None:
            Exception("obs needs to be defined")

        agents = obs
        self._n_agents = len(agents)

        goal_force = self.compute_goal_force(agents)
        social_force = self.compute_ped_repulsive_force(agents)

        summed_force = self._w_goal * goal_force + self._w_social * social_force
        action = np.concatenate([summed_force, [0]])
        return action

    def compute_goal_force(self, agents):
        # Attractive forces towards goals

        pos = agents[self._ego_id].pos_global_frame
        vel = agents[self._ego_id].vel_global_frame
        goal = agents[self._ego_id].goal_global_frame

        rgi = goal - pos
        d = np.linalg.norm(rgi)
        rgi_direction = rgi / (d + self._epsilon)

        desired_speed = self._desired_speed
        if d < 0.5:
            desired_speed = 0.1

        force = (rgi_direction * desired_speed - vel) / self._rel_time
        return force

    def compute_ped_repulsive_force(self, agents):
        # computes the repulsive force from pedestrians
        force = np.zeros((2,))
        ego_pos = agents[self._ego_id].pos_global_frame
        ego_vel = agents[self._ego_id].vel_global_frame
        ego_radius = agents[self._ego_id].radius
        
        for i, agent in enumerate(agents):
            if i != self._ego_id:
                other_pos = agents[i].pos_global_frame
                other_vel = agents[i].vel_global_frame
                other_radius = agents[i].radius

                rij = other_pos - ego_pos
                d = np.linalg.norm(rij)
                rij_direction = rij /(d + self._epsilon)
                d_without_radius = d - ego_radius - other_radius - 0.1

                vij = ego_vel - other_vel
                vd = np.linalg.norm(vij)
                vij_direction = vij /(vd + self._epsilon)

                interaction = self._lambdaImportance * vij_direction + rij_direction
                interaction_length = np.linalg.norm(interaction)
                interaction_direction = interaction / (interaction_length + self._epsilon)

                v = interaction
                w = rij

                cross_product = v[0] * w[1] - v[1] * w[0]

                dot_product = v[0] * w[0] + v[1] * w[1]

                theta = np.arctan2(cross_product, dot_product)

                B = self._gamma * interaction_length + self._epsilon

                theta_ = theta + B * self._eps

                v_input = -d_without_radius / B - (self._n_prime * B * theta_) * (self._n_prime * B * theta_)
                a_input = -d_without_radius / B - (self._n * B * theta_) * (self._n * B * theta_)
                forceVelocityAmount = - self._A * np.exp(v_input)
                forceAngleAmount = - self._A * theta_/(np.linalg.norm(theta_) + self._epsilon) * np.exp(a_input)

                forceVelocity = forceVelocityAmount * (interaction_direction)
                forceAngle = forceAngleAmount * perpendicular(interaction_direction)

                force += forceVelocity + forceAngle

        return force






    def reset(self):
        pass