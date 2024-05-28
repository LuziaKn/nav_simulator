import numpy as np
from nav_simulator.sensors.Sensor import Sensor
class OtherAgentsStatesSensor(Sensor):

    def __init__(self):
        super(OtherAgentsStatesSensor, self).__init__()
        self.sensor_type = "OtherAgentsStatesSensor"
        self.max_num_other_agents_observed = 2
        self.sorting_function = 'closest_agent_first'

    def sense(self, agents, agent_index):

        host_agent = agents[agent_index]
        other_agent_dists = {}

        other_agents_states = np.zeros((self.max_num_other_agents_observed, 7))
        other_agents_states[:,:2] = [200, 200]
        other_agents_states[:,6] = np.sqrt(200**2 + 200**2)
        for i, other_agent in enumerate(agents):
            if other_agent.id == host_agent.id:
                continue
            rel_pos_to_other_global_frame = other_agent.pos_global_frame - \
                host_agent.pos_global_frame

            rel_heading_angle = other_agent.heading_global_frame - \
                host_agent.heading_global_frame

            rel_vel_to_other_global_frame = other_agent.vel_global_frame - \
                host_agent.vel_global_frame

            rel_angular_vel = other_agent.angular_speed_global_frame - host_agent.angular_speed_global_frame

            dist_between_agent_centers = np.linalg.norm(rel_pos_to_other_global_frame)
            dist2other = dist_between_agent_centers - host_agent.radius - other_agent.radius

            other_agents_states[i,:2] = other_agent.pos_global_frame #rel_pos_to_other_global_frame
            other_agents_states[i,2] = other_agent.heading_global_frame
            other_agents_states[i,3:5] = other_agent.vel_global_frame#rel_vel_to_other_global_frame
            other_agents_states[i,5] = other_agent.angular_speed_global_frame#rel_angular_vel
            other_agents_states[i,6] = dist2other
        
        other_agents_states =  np.delete(other_agents_states, host_agent.id, axis=0)
        other_agents_states_sorted = self.closest_agent_first(other_agents_states)

        self.other_agents_states = other_agents_states_sorted[:self.max_num_other_agents_observed,:-1]

    def closest_agent_first(self, other_agent_dists):
        return other_agent_dists[other_agent_dists[:,6].argsort()]

    def get_obs(self):
        return self.other_agents_states