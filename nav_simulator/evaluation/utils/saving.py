def save_stats_txt(save_path, file_name, times_to_goals, min_dist, collision_ped_episodes, collision_robot_episodes, traveled_dist, i ):
    f = open(save_path + file_name, 'a')
    f.write('Episode number: ' + str(i) + '\n')
    f.write('time to goals: ' + str(times_to_goals[-1]) + '\n')
    f.write('min distance: ' + str(min_dist[-1]) + '\n')
    f.write('collision_ped: ' + str(collision_ped_episodes[-1]) + '\n')
    f.write('collision_robot: ' + str(collision_robot_episodes[-1]) + '\n')
    f.write('traveled dist: ' + str(traveled_dist[-1]) + '\n')




    f.close()