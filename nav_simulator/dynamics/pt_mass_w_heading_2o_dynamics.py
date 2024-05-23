import numpy as np
class PtMassWithHeading2OrderDynamics(object):
    def __init__(
        self,
        host_agent,
        config,

    ):
        self.dt = config['env']['dt']
        self.agent = host_agent
        states_lb = config['robot']['state_constraints']['lower_bounds']
        states_ub = config['robot']['state_constraints']['upper_bounds']
        self.vel_limits = np.array([[states_lb['v_x'], states_ub['v_x']],
                                    [states_lb['v_y'], states_ub['v_y']],
                                    [states_lb['w'], states_ub['w']]])
        acc_limits = np.array([[-np.inf, np.inf],\
                             [-np.inf, np.inf],\
                             [-np.inf, np.inf]])
        self.acc_limits = acc_limits

    def step(self, action: np.ndarray) -> None:
        # Limit acceleration
        # clip the action elementwise
        action = np.clip(action, self.acc_limits[:,0], self.acc_limits[:,1])

        # Compute new velocity
        selected_vels = self.agent.vel_global_frame + action[:2] * self.dt

        selected_angular_speed = self.agent.angular_speed_global_frame + action[2] * self.dt

        clipped_vels = np.clip(selected_vels, self.vel_limits[:2,0], self.vel_limits[:2,1])
        clipped_ang_speed = np.clip(selected_angular_speed, self.vel_limits[2,0], self.vel_limits[2,1])

        self.agent.pos_global_frame +=self.agent.vel_global_frame* self.dt
        self.agent.vel_global_frame = clipped_vels

        self.agent.heading_global_frame += selected_angular_speed * self.dt
        self.agent.angular_speed_global_frame = clipped_ang_speed

        self.agent.speed_global_frame = np.linalg.norm(clipped_vels)

