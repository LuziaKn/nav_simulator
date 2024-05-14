import numpy as np

def _check_if_at_goal(agent):
    is_near_goal = (agent.pos_global_frame[0] - agent.goal_global_frame[0]) ** 2 + (
                agent.pos_global_frame[1] - agent.goal_global_frame[1]) ** 2 <= agent.near_goal_threshold ** 2
    agent.is_at_goal = is_near_goal
    if agent.is_at_goal:
        #agent.pref_speed = 0.0
        print("Agent {} reached the goal".format(agent.id))