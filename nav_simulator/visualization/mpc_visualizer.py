from nav_simulator.visualization.matplotlib_visualizer import Visualizer
from nav_simulator.utils.utils import marker_size_in_figure_coords

class MPCVisualizer(Visualizer):
    def __init__(self, save_dir, config, limits, fig_size, save_figures, save_for_animation, save_every_n_plots,  keep_frames, replay, debug, show):
        super(MPCVisualizer, self).__init__(save_dir, limits, fig_size, save_figures, save_for_animation,save_every_n_plots,  keep_frames, replay, debug, show)

        self.config = config
        self._N = config['mpc']['time_horizon']


    def init_episode_plot(self, agents):
        super(MPCVisualizer, self).init_episode_plot(agents)

        # initialize plan plot
        ag_id = 0
        agent = agents[ag_id]
        color = self._plt_colors[self._ego_color]
        self.plan_circles = [self.ax.plot([], [], 'o', color=color, alpha=0.3, markersize=marker_size_in_figure_coords(self._fig_size_points, agent.radius))[0] for k  in range(self._N)]


    def update_episode_plot(self, agents, current_step, episode_number, experiment_id=None,**kwargs):


        # update plan plot
        agent = agents[0]
        if 'plot_infos_dict' in kwargs:
            if 'output' in kwargs['plot_infos_dict']:
                plan = kwargs['plot_infos_dict']['output']

                for k in range(1,self._N):
                    self.plan_circles[k].set_data(plan[k,0], plan[k, 1])

        super(MPCVisualizer, self).update_episode_plot(agents, current_step, episode_number, experiment_id)


        if self.save_figures:
            self.save_figure(current_step, episode_number, experiment_id)

        if self.save_for_animation:
            self.save_figures_for_animation(current_step, episode_number, experiment_id)




