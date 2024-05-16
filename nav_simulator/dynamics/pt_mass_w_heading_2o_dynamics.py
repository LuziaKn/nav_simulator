import numpy as np
class PtMassWithHeading2OrderDynamics(object):
    def __init__(
        self,
        dt,
        agent,
        vel_limits=np.array([[-np.inf, np.inf], [-np.inf, np.inf], [-np.inf, np.inf]]),
        acc_limits=np.array([[-np.inf, np.inf], [-np.inf, np.inf], [-np.inf, np.inf]]),
    ):
        self.dt = dt
        self.agent = agent
        self.vel_limits = vel_limits
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

