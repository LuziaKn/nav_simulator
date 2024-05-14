import numpy as np
from nav_simulator.sensors.Sensor import Sensor
class OtherAgentsStatesSensor(Sensor):

    def __init__(self):
        super(OtherAgentsStatesSensor, self).__init__()
        self.sensor_type = "OtherAgentsStates"
        self.max_num_other_agents_observed = 2

    def sense(self, agents, agent_index):

        host_agent = agents[agent_index]
        other_agent_dists = {}

        other_agents_states = np.zeros((self.max_num_other_agents_observed, 7))
        for i, other_agent in enumerate(agents):
            if other_agent.id == host_agent.id:
                continue
            rel_pos_to_other_global_frame = other_agent.pos_global_frame - \
                host_agent.pos_global_frame

            dist_between_agent_centers = np.linalg.norm(rel_pos_to_other_global_frame)
            dist2other = dist_between_agent_centers - host_agent.radius - other_agent.radius

            other_agents_states[i,:] = rel_pos_to_other_global_frame

