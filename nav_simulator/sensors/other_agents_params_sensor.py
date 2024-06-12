import numpy as np
from nav_simulator.sensors.Sensor import Sensor

class OtherAgentsParamsSensor(Sensor):

    def __init__(self):
        super(OtherAgentsParamsSensor, self).__init__()
        self.sensor_type = "OtherAgentsParamsSensor"
        self.max_num_other_agents_observed = 4
        self.sorting_function = 'closest_agent_first'

    def sense(self, agents, agent_index):

        host_agent = agents[agent_index]
        other_agent_dists = {}

        other_agents_states = np.zeros((self.max_num_other_agents_observed, 6))
        other_agents_states[:,:2] = [200, 200]
        other_agents_states[:,5] = np.sqrt(200**2 + 200**2)
        for i, other_agent in enumerate(agents):
            if i<self.max_num_other_agents_observed:
                if other_agent.id == host_agent.id:
                    continue
                rel_pos_to_other_global_frame = other_agent.pos_global_frame - \
                    host_agent.pos_global_frame

                dist_between_agent_centers = np.linalg.norm(rel_pos_to_other_global_frame)
                dist2other = dist_between_agent_centers - host_agent.radius - other_agent.radius

                other_agents_states[i,:2] = other_agent.policy._goal
                other_agents_states[i,2] = other_agent.policy._desired_speed
                other_agents_states[i,3] = other_agent.policy._w_goal
                other_agents_states[i,4] = other_agent.policy._w_social
                other_agents_states[i,5] = dist2other
        
        other_agents_states =  np.delete(other_agents_states, host_agent.id, axis=0)
        other_agents_states_sorted = self.closest_agent_first(other_agents_states) # to do sorted

        self.other_agents_params = other_agents_states_sorted[:self.max_num_other_agents_observed,:-1]
        self.other_agents_params = other_agents_states[:self.max_num_other_agents_observed, :-1]

    def closest_agent_first(self, other_agent_dists):
        return other_agent_dists[other_agent_dists[:,5].argsort()]

    def get_obs(self):
        return self.other_agents_params