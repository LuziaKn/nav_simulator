import numpy as np

def _check_if_at_goal(agent, obs=None):
    is_near_goal = (agent.pos_global_frame[0] - agent.goal_global_frame[0]) ** 2 + (
                agent.pos_global_frame[1] - agent.goal_global_frame[1]) ** 2 <= agent.near_goal_threshold ** 2
    agent.is_at_goal = is_near_goal
    agent.done = is_near_goal
    if agent.is_at_goal:
        #agent.pref_speed = 0.0
        print("Agent {} reached the goal".format(agent.id))

def _check_if_in_collision(agent, obs=None):
    for i in range(len(obs)):
        if i != agent.id:
            dist = np.linalg.norm(agent.pos_global_frame - obs[i].pos_global_frame)
            if dist < agent.radius + obs[i].radius:
                if i == 0:
                    agent.in_collision_with_robot = True
                else:
                    agent.in_collision_with_pedestrian = True
                #agent.done = True
                print("Agent {} collided with agent {}".format(agent.id, i))




