import random
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

POINT_PRECISION = 5
PI = 3.1415926535
POINTS = 20_000
POINTS_PER_FRAME = 20
POINT_SPACING = int(POINTS/POINTS_PER_FRAME)


def get_random_points():
    return random.random()*random.choice([-1, 1]), random.random()*random.choice([-1, 1])


def init_plot(line, ax):
    """
    Initializes the animation plot
    ax[1] refers to the approximation graph
    ax[0] refers to the scatter plot
    """
    ylim = [3.08, 3.20]
    font_dict = {'fontsize': 13, 'weight': 'bold'}
    plt.xticks(fontsize=13)
    plt.yticks(fontsize=13)
    ax[1].set_xlim(0, POINTS)
    ax[1].set(ylim=ylim)
    ax[1].set_xlabel('\nPoints Simulated', fontdict=font_dict)
    ax[1].set_ylabel('Estimated Value\n', fontdict=font_dict)
    ax[1].axhline(y=PI, color='r', linestyle='-')
    ax[1].legend(['Estimations', 'Value of π'])
    ax[0].set_xlim(-1, 1)
    ax[0].set_ylim(-1, 1)
    ax[0].axis('square')
    ax[0].set_xticks([])
    ax[0].set_yticks([])
    return line


def update_func(frame, sc_list, circle_graph, approx_pi_graph, approx_graph):
    frame = int(frame+1)
    apgx = approx_pi_graph['x'][:frame]
    apgy = approx_pi_graph['y'][:frame]
    cgx = circle_graph['x'][:frame]
    cgy = circle_graph['y'][:frame]

    ax_title = f'π estimate = {apgy[-1]:4f}   Error = {abs((PI - apgy[-1])):4f}'
    approx_graph.set_title(ax_title)

    line[0].set_offsets(np.c_[cgx, cgy])  # setting sactter plot coordinates
    line[0].set_array(sc_list[:frame])  # setting color array for scatter plot
    line[1].set_data(apgx, apgy)  # setting approximation graph coordinates
    return line


def get_plot_details():
    """
    Simulates all the points & calculates the estimated value
    before the animation begins
    """
    sc_list = []  # array of colors for scatter plot points
    points_in_circle = 0  # count of number of points in circle
    circle_graph = {'x': [], 'y': []}
    approx_pi_graph = {'x': [], 'y': []}
    for point_cumulative in range(1, POINTS+1):
        point_x, point_y = get_random_points()
        circle_graph['x'].append(point_x)
        circle_graph['y'].append(point_y)
        if point_x**2 + point_y**2 <= 1:  # if point is inside unit circle
            sc_list.append(0)  # point's color will be cyan
            points_in_circle += 1
        else:
            sc_list.append(1)  # else point's color will be purple
        probability = points_in_circle / point_cumulative
        pi_approx_val = probability * 4
        approx_pi_graph['x'].append(point_cumulative)
        approx_pi_graph['y'].append(pi_approx_val)
    return sc_list, circle_graph, approx_pi_graph


if __name__ == '__main__':

    fig, (ax_circle, ax_graph) = plt.subplots(1, 2)
    line_circle = ax_circle.scatter([], [],  # circle scatter plot
                                    marker=".", c=[],
                                    cmap='cool',
                                    vmin=0, vmax=1)  # 0: cyan, 1: purple
    line_graph, = ax_graph.plot([], [], 'g', linewidth=1.0)  # approx graph
    ax = (ax_circle, ax_graph)
    line = (line_circle, line_graph)
    fargs = *get_plot_details(), ax[1]
    ani = FuncAnimation(fig,
                        func=update_func,
                        fargs=fargs,
                        frames=np.linspace(0, POINTS, POINT_SPACING + 1),
                        init_func=lambda: init_plot(line, ax),
                        blit=False,
                        repeat=False,
                        interval=50)

    plt.rcParams.update({'font.size': 13, 'font.weight': 'bold'})
    plt.tight_layout()
    mng = plt.get_current_fig_manager()
    mng.window.showMaximized()
    plt.grid()
    plt.show()
