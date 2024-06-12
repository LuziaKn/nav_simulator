def save_stats_txt(save_path, file_name, times_to_goals, i ):
    f = open(save_path + file_name, 'a')
    f.write('Episode number: ' + str(i) + '\n')
    f.write('time to goals: ' + str(times_to_goals[-1]) + '\n')

    f.close()