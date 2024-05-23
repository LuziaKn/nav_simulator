import importlib
import numpy as np
def str_to_class(modulename, classname):
    return getattr(importlib.import_module(modulename), classname)

def next_even_number(number):
    if number % 2 == 0:
        return number + 0
    else:
        return number + 1

def perpendicular(a):
    # returns the vector perpendicular to a (left)
    b = np.zeros_like(a)
    b[0] = -a[1]
    b[1] = a[0]
    return b

def marker_size_in_figure_coords(fig_size_points, desired_markersize_fig_coords=1):
    desired_markersize_fig_coords
    markersize = fig_size_points[0] * desired_markersize_fig_coords / 10
    return markersize

def get_plotting_colors():
    plt_colors = []
    plt_colors.append([0.0, 0.4470, 0.7410])  # blue
    plt_colors.append([0.8500, 0.3250, 0.0980])  # orange
    plt_colors.append([0.4660, 0.6740, 0.1880])  # green
    plt_colors.append([0.4940, 0.1840, 0.5560])  # purple
    plt_colors.append([0.9290, 0.6940, 0.1250])  # yellow
    plt_colors.append([0.3010, 0.7450, 0.9330])  # cyan
    plt_colors.append([0.6350, 0.0780, 0.1840])  # chocolate
    plt_colors.append([1, 0, 0])  # red
    plt_colors.append([0, 0, 0])  # black
    plt_colors.append([129 / 255, 133 / 255, 137 / 255])  # gray
    plt_colors.append([102 / 255, 153 / 255, 204 / 255])  # light blue
    return plt_colors