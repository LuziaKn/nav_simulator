import numpy as np
class PtMassWithHeading2OrderDynamics(object):
    def __init__(
        self,
        host_agent,
        env_config,

    ):
        self.dt = env_config['dt']
        self.agent = host_agent
        self.agent_type = self.agent.type
        if self.agent_type == 'robot':
            state_constr = env_config['robot']['state_constraints']
            input_contr = env_config['robot']['input_constraints']
        elif self.agent_type == 'pedestrian':
            state_constr = env_config['pedestrian']['state_constraints']
            input_contr = env_config['pedestrian']['input_constraints']
        self.vel_limits = np.array([[state_constr['lower_bounds']['v_x'], state_constr['upper_bounds']['v_x']],
                                    [state_constr['lower_bounds']['v_y'], state_constr['upper_bounds']['v_y']],
                                    [state_constr['lower_bounds']['w'], state_constr['upper_bounds']['w']]])
        self.acc_limits = np.array([[input_contr['lower_bounds']['a_x'], input_contr['upper_bounds']['a_x']],
                             [input_contr['lower_bounds']['a_y'], input_contr['upper_bounds']['a_y']],
                             [input_contr['lower_bounds']['alpha'], input_contr['upper_bounds']['alpha']]])



    def step(self, action: np.ndarray) -> None:
        # Limit acceleration
        # clip the action elementwise
        #breakpoint()
        action = np.clip(action, self.acc_limits[:,0], self.acc_limits[:,1])

        # Compute new velocity
        selected_vels = self.agent.vel_global_frame + action[:2] * self.dt

        selected_angular_speed = self.agent.angular_speed_global_frame + action[2] * self.dt

        clipped_vels = selected_vels#np.clip(selected_vels, self.vel_limits[:2,0], self.vel_limits[:2,1])
        clipped_ang_speed = selected_angular_speed #np.clip(selected_angular_speed, self.vel_limits[2,0], self.vel_limits[2,1])

        self.agent.pos_global_frame +=self.agent.vel_global_frame* self.dt
        self.agent.vel_global_frame = clipped_vels

        self.agent.heading_global_frame += selected_angular_speed * self.dt
        self.agent.angular_speed_global_frame = clipped_ang_speed

        self.agent.speed_global_frame = np.linalg.norm(clipped_vels)


