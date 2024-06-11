import numpy as np
from sys import platform
import time


if platform == "darwin":
    import matplotlib as mpl
    mpl.use('TkAgg')
import matplotlib.pyplot as plt
import matplotlib
import time
import os
import glob
import imageio
import matplotlib.patches as mpatches
from matplotlib.lines import Line2D
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.collections import LineCollection, PatchCollection
from matplotlib.colors import Normalize
from matplotlib.patches import Circle
import matplotlib.animation as animation
import matplotlib.ticker as ticker
import shutil
from mpl_toolkits.axes_grid1 import make_axes_locatable
from abc import ABC
import seaborn as sns
sns.set()

from nav_simulator.utils.utils import marker_size_in_figure_coords, get_plotting_colors

matplotlib.rcParams.update({'font.size': 24})



class Visualizer():
    def __init__(self, plot_save_dir, env_config, limits=None, fig_size=(5, 5), save_figures=True, save_for_animation=False, save_every_n_plots=4, keep_frames=False, replay=False, show=False, debug = False):
        self.plot_save_dir=plot_save_dir
        self.collision_plot_dir=plot_save_dir + "/collisions/"
        self.limits = limits
        self.fig_size=fig_size
        self.save_figures = save_figures
        self.save_for_animation = save_for_animation
        self.save_every_n_plots = save_every_n_plots
        self.keep_frames = keep_frames
        self.replay = replay
        self.show = show
        self.debug = debug
        colors = ['blue', 'red']
        self.cmap = LinearSegmentedColormap.from_list('custom_cmap', colors)


        self.fig = plt.figure(figsize=self.fig_size)
        self.ax = self.fig.add_subplot(1, 1, 1)

        if self.limits is not None:
            xlim, ylim = self.limits
            self.ax.set_xlim(xlim)
            self.ax.set_ylim(ylim)
            self.ax.set_aspect('equal')
        else:
            self.ax.axis('equal')

        self._ego_color = 0
        self._others_color = 1

        # Get the size of the plot area in inches
        fig_size_inches = self.fig.get_size_inches()

        # Get the DPI (dots per inch) of the figure
        dpi = self.fig.get_dpi()

        # Convert the figure size from inches to points
        self._fig_size_points = fig_size_inches * dpi

        #self.img = self.ax.imshow(X, vmin=-1, vmax=1, interpolation="None", cmap="RdBu")
        self.base_fig_name = "{test_case}_{experiment_id}_{n_agents}agents_{step}.{extension}"

        self._plt_colors = get_plotting_colors()

        plt.show(block=False)

    def init_episode_plot(self, agents):

        self._n_agents = len(agents)

        # set colors
        color_ids = []
        for agent in agents:
            color_ids.append(self._ego_color if agent.id == 0 else self._others_color)
        colors = [self._plt_colors[index] for index in color_ids]

        # initialize goals
        self.goals = [self.ax.scatter(agent.goal_global_frame[0], agent.goal_global_frame[1], s=300, c=colors[agent.id], marker='x',
                        clip_on=False) for agent in agents]

        # initialize circles representing agents
        self.circles = [self.ax.plot([], [], 'o', markersize=marker_size_in_figure_coords(self._fig_size_points, agent.radius))[0] for agent in agents]



    def plot_episodes(self, traj_data, agents, episode_number, save_dir='', debug=False):
        for e in range(traj_data.shape[0]):
            self.update_episode_plot(traj_data,
                              current_step = e,
                              agents=agents,
                              episode_number=episode_number)

    def update_episode_plot(self, agents, current_step, episode_number, experiment_id=None, save = False, reset=True, grayscale=False, **kwargs):

        # Update circles representing agents
        for agent, circle in zip(agents, self.circles):
            circle.set_data(agent.pos_global_frame[0], agent.pos_global_frame[1])
        self.fig.canvas.draw()
        self.fig.canvas.flush_events()
   

        # save the figure
        if save:
            if self.save_figures:
                self.save_figure(current_step, episode_number, experiment_id)

            if self.save_for_animation:
                self.save_figures_for_animation(current_step, episode_number, experiment_id)

        

    def save_figure(self, current_step, episode_number, experiment_id=None):
        if experiment_id is not None:
            base_fig_name = "{test_case}_{experiment_id}_{n_agents}agents_{step}.{extension}"
        else:
            base_fig_name = "{test_case}_{n_agents}agents_{step}.{extension}"

        if not os.path.exists(self.plot_save_dir):
            os.makedirs(self.plot_save_dir)

        fig_name = base_fig_name.format(
            test_case=str(episode_number).zfill(3),
            n_agents=self._n_agents,
            experiment_id=experiment_id,
            step="",
            extension='png')

        fig_name = os.path.join(self.plot_save_dir, fig_name)
        self.fig.savefig(fig_name)
        print("Saved figure in", fig_name)

    def save_figures_for_animation(self, current_step, episode_number, experiment_id=None):
        if current_step/self.save_every_n_plots != 0:
            if experiment_id is not None:
                base_fig_name = "{test_case}_{experiment_id}_{n_agents}agents_{step}.{extension}"
            else:
                base_fig_name = "{test_case}_{n_agents}agents_{step}.{extension}"

            if not os.path.exists(self.plot_save_dir):
                os.makedirs(self.plot_save_dir)

            fig_name = base_fig_name.format(
                test_case=str(episode_number).zfill(3),
                n_agents=self._n_agents,
                experiment_id=experiment_id,
                step=str(current_step).zfill(3),
                extension='png')

            fig_name = os.path.join(self.plot_save_dir, fig_name)
            self.fig.savefig(fig_name)
            print("Saved figure in", fig_name)

    def animate_episode(self, n_agents,episode,ego_policy, ego_planning_type, others_policy, was_in_collision=False, experiment_id=None):

        if experiment_id is not None:
            base_fig_name = "{test_case}_{experiment_id}_{n_agents}agents_{step}.{extension}"
        else:
            base_fig_name = "{test_case}_{n_agents}agents_{step}.{extension}"

        if not os.path.exists(self.plot_save_dir):
            os.makedirs(self.plot_save_dir)

        # Load all images of the current episode (each animation)
        fig_name = base_fig_name.format(
            test_case=str(episode).zfill(3),
            n_agents=n_agents,
            experiment_id=experiment_id,
            step="_*",
            extension='png')
        last_fig_name = base_fig_name.format(
            test_case=str(episode).zfill(3),
            experiment_id=experiment_id,
            n_agents=n_agents,
            step="",
            extension='png')
        all_filenames = self.plot_save_dir + fig_name
        last_filename = self.plot_save_dir + last_fig_name

        animation_filename = base_fig_name.format(
            test_case=str(episode).zfill(3),
            n_agents=n_agents,
            experiment_id=experiment_id,
            step="",
            extension='gif')

        # Dump all those images into a gif (sorted by timestep)
        filenames = glob.glob(all_filenames)
        filenames.sort()
        images = []
        if self.replay:
            animation_img_save_dir = self.plot_save_dir + "frames"
        else:
            animation_img_save_dir = self.plot_save_dir + animation_filename.split(".")[0]+ "/frames"
        os.makedirs(animation_img_save_dir, exist_ok=True)
        for filename in filenames:
            images.append(imageio.imread(filename))
            if self.keep_frames:
                shutil.move(filename, animation_img_save_dir + "/" + filename.split("/")[-1])
            else:
                os.remove(filename)
        for i in range(10):
            images.append(imageio.imread(last_filename))

        # Save the gif in a new animations sub-folder
        if self.replay:
            animation_save_dir = self.plot_save_dir
        else:
            animation_save_dir = self.plot_save_dir + "/gifs/"
        if was_in_collision:
            animation_save_dir =  self.plot_save_dir + "/gifs/collisions/"
        os.makedirs(animation_save_dir, exist_ok=True)
        animation_filename = os.path.join(animation_save_dir, animation_filename)
        print("Saving the gif in", animation_filename)
        imageio.mimsave(animation_filename, images)


    def remove_patch_collection(self):
        if self.patch_collection is not None:
            self.patch_collection.remove()
            self.patch_collection = None

    def draw_plan(self, output):
        # Pre-calculate colors
        if self.ego_color == 0:
            plt_color = rgba2rgb(plt_colors[self.ego_color] + [0.5])
            edge_color = rgba2rgb(plt_colors[self.ego_color] + [0.4])
        else:
            plt_color = rgba2rgb(plt_colors[self.ego_color] + [0.2])
            edge_color = rgba2rgb(plt_colors[self.ego_color] + [0.1])

        # Create circles for all points at once
        circles = [
            plt.Circle(output[iter][4:6], radius=0.5, fc=plt_color, ec=edge_color, alpha=0.2)
            for iter in range(output.shape[0])
        ]

        # Add all circles to the plot at once
        for circle in circles:
            self.ax.add_patch(circle)

    def draw_constraints(self):
        linear_constraints = [[0, 1.5, -1, 0], [0, -1.5, 1, 0]]

        for linear_constraint in  linear_constraints:
            constraint_pt = linear_constraint[:2]
            constraint_dir = linear_constraint[2:]
            radius_shift_x = -0.25 * np.sign(constraint_dir[1])
            radius_shift_y = -0.25 * np.sign(constraint_dir[0])
            self.ax.plot(np.array([constraint_pt[0]+radius_shift_x, constraint_pt[0]+radius_shift_x + 4*constraint_dir[0], constraint_pt[0]+radius_shift_x - 4*constraint_dir[0]]),
                         np.array([constraint_pt[1]+radius_shift_y, constraint_pt[1]+radius_shift_y + 4*constraint_dir[1], constraint_pt[1]+radius_shift_y - 4*constraint_dir[1]]), color='black',
                         ls='-', linewidth=2)

    def draw_initial_guess(self, initial_guess):
        for i in range(int(initial_guess.shape[1]/5)):
            initial_guess_i = initial_guess[:,i*5:i*5+2]

            if i == 0:
                color_ind = self.ego_color
            else:
                color_ind = self.others_color
            plt_color = plt_colors[color_ind]
            beta = 0.5
            alpha = 0.2

            # plot line
            self.ax.plot(initial_guess_i[:,0], initial_guess_i[:,1], color=plt_color, ls='-', linewidth=1)

    def draw_goals(self, agents, grayscale=False):

        for agent in agents:
            goal = agent.goal_global_frame
            # draw goal
            if agent.id==0:
                color_ind = 0
            else:
                color_ind = 1
            plt_color = plt_colors[color_ind]
            if grayscale:
                plt_color = plt_colors[9]
            # draw agent number

            self.ax.scatter(goal[0], goal[1], s=300, c=plt_color, marker='x',
                        clip_on=False)
            self.ax.scatter(goal[0], goal[1], s=200, c='1', edgecolors=plt_color,
                        marker='o',
                        clip_on=False, )
            self.ax.text(goal[0]+0.01, goal[1]-0.01, str(agent.id), ha="center", va="center",
                     color=plt_color, fontsize=12, zorder=1)

            # # draw estimated goals
            # if config.EvaluationConfig.apply_mpc_est_interactive_predictions:
            #     if hasattr(agents[0].policy, 'agents_char_estimated'):
            #         estimated_goal = agents[0].policy.agents_char_estimated['goal_global_frame'][i, :]
            #         plt.text(estimated_goal[0], estimated_goal[1], str(agent.id), ha="center", va="center",
            #                  color="black", fontsize=12, alpha=0.5)
            #         plt.scatter(estimated_goal[0], estimated_goal[1], s=200, c='1', edgecolors=plt_color,
            #                     marker='o',
            #                     clip_on=False, alpha=0.5)

    def draw_legend(self, agent_data, ego_id, others_id):
        ego = plt.Circle([-100, -100],
                         radius=agent_data[0]['radius'], fc=plt_colors[ego_id], ec=plt_colors[ego_id])
        others = plt.Circle([-100, -100],
                            radius=agent_data[0]['radius'], fc=plt_colors[others_id], ec=plt_colors[others_id])
        goal_icon_cross = self.ax.scatter(-100, -100, s=300, c=plt_colors[9], marker='x',
                                      clip_on=False)
        goal_marker_circle = self.ax.scatter(-100, -100, s=200, c='1', edgecolors=plt_colors[9],
                                         marker='o',
                                         clip_on=False)
        goal_marker_text = self.ax.text(-100, -100, "i", ha="center", va="center",
                                    color="black", fontsize=12, alpha=0.5)
        vel_lin = Line2D([-100, -100], [-101, -102], color=plt_colors[9], linewidth=2)

        obstacle_lin = Line2D([-100, -100], [-101, -102], color='black', linewidth=2)

        beta = 0.5
        ego_plan = plt.Circle([-100, -100],
                         radius=agent_data[0]['radius'], fc=plt_colors[ego_id]+[float(beta)], ec=plt_colors[ego_id]+[float(beta)-0.1])

        others_plan = plt.Circle([-100, -100],
                         radius=agent_data[0]['radius'], fc=plt_colors[others_id]+[float(beta)], ec=plt_colors[others_id]+[float(beta)-0.1])
        others_plan_uncertainty = plt.Circle([-100, -100], radius=agent_data[0]['radius']+0.3, fill=False,
                                        ec=plt_colors[others_id]+[float(beta)])


        self.ax.legend(handles=[ego, ego_plan, others, (others_plan, others_plan_uncertainty),  (goal_icon_cross, goal_marker_circle), vel_lin, obstacle_lin],
                   labels=['Robot Position', 'Robot Plan',  'SF Agent Position', 'SF Agent Uncertain Predictions', 'Goal', 'Velocity Vector','Wall'], fontsize=12, loc='upper right', ncol=2)


    def plot_times(self, agents, e, times):
        for agent in agents:
            current_position = agent.pos_global_frame
            self.ax.text(current_position[0]-0.2, current_position[1]-0.2, str(round(times[agent.id],1)), ha="center", va="center",
                     color="black", fontsize=12)



def draw_static_constraints(agents):



    # Display closest points
    for i in range(len(agents)):
        color_ind = i % len(plt_colors)
        plt_color = plt_colors[color_ind]

        if hasattr(agents[i].policy, 'constr_visualization'):
            constr_visualization = agents[i].policy.constr_visualization
            # closest_points.append(np.zeros(2))
            if (
                    constr_visualization is not None
                    and "closest_points" in constr_visualization
            ):
                closest_points = constr_visualization["closest_points"]
                for pt in closest_points:
                    plt.plot(pt[0], pt[1], 'o--',color = plt_color, linewidth=2, markersize=12)


        linear_con_a = agents[i].policy.linear_constraints['a']
        linear_con_b = agents[i].policy.linear_constraints['b']
        for j in range(len(linear_con_b)):
            x1 = -5
            x2 = 5
            radius = agents[i].radius
            alpha = np.arctan2(-linear_con_a[j][0], linear_con_a[j][1])
            #h = radius / np.sin(alpha)
            #linear_con_b[i] = linear_con_b[i] - h * linear_con_a[i][1]

            if linear_con_a[j][0] == 0 and linear_con_a[j][1] !=0:
                y1 = linear_con_b[j]/linear_con_a[j][1]
                y2 = linear_con_b[j]/linear_con_a[j][1]
            elif linear_con_a[j][1] !=0:
                y1 = -linear_con_a[j][0]/linear_con_a[j][1]* x1 + linear_con_b[j]/linear_con_a[j][1]
                y2 = -linear_con_a[j][0] / linear_con_a[j][1] * x2 + linear_con_b[j] / linear_con_a[j][1]
            else:
                x1 = linear_con_b[j]/linear_con_a[j][0]
                x2 = linear_con_b[j] / linear_con_a[j][0]
                y1 = 2
                y2 = -2


            plt.plot(np.array([x1, x2]), np.array([y1, y2]), color=plt_colors[i], ls='-', linewidth=2)
def draw_constraints(agents):
    i = 0


    if hasattr(agents[0].policy, 'predicted_traj'):
        for id in range(1,agents[0].policy.predicted_traj_others.shape[0]):
            for (pos, pos_obst) in zip(agents[0].policy.predicted_traj, agents[0].policy.predicted_traj_others[id]):
                plt_color = plt_colors[1]
                # draw constraint
                r_robot = agents[0].radius + agents[0].policy.radius_enlargement
                r_obst = agents[1].radius + agents[0].policy.radius_enlargement
                diff = pos - pos_obst
                diff_norm = diff / np.linalg.norm(diff)
                point = pos_obst + (r_obst + r_robot) * diff / np.linalg.norm(diff)

                diff_point_pos = point - pos

                a = -diff_norm * np.linalg.norm(diff_point_pos)
                a /= np.linalg.norm(a)

                angle = 0
                a_x = a[0] * np.cos(angle) + (-1) * a[1] * np.sin(angle)
                a_y = np.sin(angle) * a[0] + np.cos(angle) * a[1]
                a_rotated = a

                a = a_rotated
                b = a.T @ point

                error = a[0] * pos[0] + a[1] * pos[1] - b
                if error < 0:
                    plt_color = plt_colors[2]
                else:
                    plt_color = plt_colors[7]

                error2 = a[0] * point[0] + a[1] * point[1] - b
                # print(error2)

                x1 = pos_obst[0] - 1
                x2 = pos_obst[0] + 1
                y1 = b / a[1] - a[0] / a[1] * (x1)
                y2 = b / a[1] - a[0] / a[1] * (x2)

                if i ==2:
                    plt.plot(np.array([x1, x2]), np.array([y1, y2]), color=plt_color, ls='-', linewidth=2)

                i += 1









def find_nearest(array,value):
    # array is a 1D np array
    # value is an scalar or 1D np array
    tiled_value = np.tile(np.expand_dims(value,axis=0).transpose(), (1,np.shape(array)[0]))
    idx = (np.abs(array-tiled_value)).argmin(axis=1)
    return array[idx], idx

def rgba2rgb(rgba):
    # rgba is a list of 4 color elements btwn [0.0, 1.0]
    # or a 2d np array (num_colors, 4)
    # returns a list of rgb values between [0.0, 1.0] accounting for alpha and background color [1, 1, 1] == WHITE
    if isinstance(rgba, list):
        alpha = rgba[3]
        r = max(min((1 - alpha) * 1.0 + alpha * rgba[0],1.0),0.0)
        g = max(min((1 - alpha) * 1.0 + alpha * rgba[1],1.0),0.0)
        b = max(min((1 - alpha) * 1.0 + alpha * rgba[2],1.0),0.0)
        return [r,g,b]
    elif rgba.ndim == 2:
        alphas = rgba[:,3]
        r = np.clip((1 - alphas) * 1.0 + alphas * rgba[:,0], 0, 1)
        g = np.clip((1 - alphas) * 1.0 + alphas * rgba[:,1], 0, 1)
        b = np.clip((1 - alphas) * 1.0 + alphas * rgba[:,2], 0, 1)
        return np.vstack([r,g,b]).T