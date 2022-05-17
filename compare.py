import random
import numpy as np
from scipy.stats import qmc
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


POW = 14  # will simulate 2^POW points
POINTS = 2**POW
PI = 3.1415926535
POINTS_PER_FRAME = 2**4  # must be a power of 2
POINT_SPACING = int(POINTS/POINTS_PER_FRAME)


def generate_sobol():
    sampler = qmc.Sobol(d=2, scramble=False)
    sample = sampler.random_base2(m=POW)
    points = {'x': [], 'y': []}
    for i in sample:
        points['x'].append(i[0])
        points['y'].append(i[1])
    return points


def pseudo_points():
    return random.random(), random.random()


def quasi_points(sobol_points):
    return sobol_points['x'].pop(), sobol_points['y'].pop()


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

    for i in [0, 2]:
        ax[i].set_xlim(0.001, 1)
        ax[i].set_ylim(0.001, 1)
        ax[i].set_xticks([])
        ax[i].set_yticks([])
        ax[i].axis('square')

    for i in [1, 3]:
        ax[i].set_xlim(0, POINTS)
        ax[i].set_ylabel('Estimated Value\n', fontdict=font_dict)
        ax[i].axhline(y=PI, color='r', linestyle='-')
        ax[i].legend(['Estimations', 'Value of π'])
        ax[i].set(ylim=ylim)

    ax[0].set_title('Pseudorandom Number Generation')
    ax[2].set_title('Quasirandom Number Generation (Sobol Sequence)')

    ax[3].set_xlabel('\nPoints Simulated', fontdict=font_dict)
    return line


def update_func(frame, pseudo_plot_detail, quasi_plot_detail, graph):
    """
    Update the animation every frame
    - pseudo_plot_details is a dict contaning 3 keys:
        `sc_list`: a color array for individual scatter plot point
        `circle_graph`: a dictionary with 'x', 'y' as key. Contains
                        coordinates for scatterplot
        `pi_graph`: a dictionary with 'x', 'y' as key. Contains
                        coordinates for pi graph

    - graph: a dict containing Axes for pseudo & quasi pi graph
            Used for updaing the title of pi graph

    """
    frame = int(frame+1)

    pseudo_sc_list = pseudo_plot_detail['sc_list']
    quasi_sc_list = quasi_plot_detail['sc_list']

    pseudo_circle_graph = pseudo_plot_detail['circle_graph']
    quasi_circle_graph = quasi_plot_detail['circle_graph']

    pseudo_pi_graph = pseudo_plot_detail['pi_graph']
    quasi_pi_graph = quasi_plot_detail['pi_graph']

    pseudo_graph_ax = graph['pseudo']
    quasi_graph_ax = graph['quasi']

    pseudo_pg_x = pseudo_pi_graph['x'][:frame]
    pseudo_pg_y = pseudo_pi_graph['y'][:frame]
    pseudo_cg_x = pseudo_circle_graph['x'][:frame]
    pseudo_cg_y = pseudo_circle_graph['y'][:frame]

    quasi_pg_x = quasi_pi_graph['x'][:frame]
    quasi_pg_y = quasi_pi_graph['y'][:frame]
    quasi_cg_x = quasi_circle_graph['x'][:frame]
    quasi_cg_y = quasi_circle_graph['y'][:frame]

    pseudo_pi = pseudo_pg_y[-1]
    quasi_pi = quasi_pg_y[-1]
    pseudo_title = f'π estimate = {pseudo_pi:4f}   Error = {abs((PI - pseudo_pi)):4f}'
    quasi_title = f'π estimate = {quasi_pi:4f}   Error = {abs((PI - quasi_pi)):4f}'
    pseudo_graph_ax.set_title(pseudo_title)
    quasi_graph_ax.set_title(quasi_title)

    # setting sactter plot coordinates for pseudo graph
    line[0].set_offsets(np.c_[pseudo_cg_x, pseudo_cg_y])
    # setting color array for pseudo scatter plot
    line[0].set_array(pseudo_sc_list[:frame])
    # setting pseudo pi approx graph coordinates
    line[1].set_data(pseudo_pg_x, pseudo_pg_y)

    # setting sactter plot coordinates for quasi graph
    line[2].set_offsets(np.c_[quasi_cg_x, quasi_cg_y])
    # setting color array for quasi scatter plot
    line[2].set_array(quasi_sc_list[:frame])
    # setting quasi pi approx graph coordinates
    line[3].set_data(quasi_pg_x, quasi_pg_y)
    return line


def get_plot_details(**kwargs):
    """
    Simulates all the points & calculates the estimated value
    before the animation begins

    Parameters:
        'func': name of the function generating random points.
                Either 'pseudo_points' or 'quasi_points'

        'sobol': an array of 2D sobol points
                Required if `func`= quasi_points
    """
    sobol_points = kwargs.get('sobol', None)
    func = kwargs.get('func', None)  # funct to use for random point generation
    sc_list = []  # array of colors for scatter plot points
    points_in_circle = 0  # count of number of points in circle
    circle_graph = {'x': [], 'y': []}
    pi_graph = {'x': [], 'y': []}

    for point_cumulative in range(1, POINTS+1):
        if sobol_points is None:
            point_x, point_y = func()
        else:
            point_x, point_y = func(sobol_points)

        circle_graph['x'].append(point_x)
        circle_graph['y'].append(point_y)

        if point_x**2 + point_y**2 <= 1:  # if point is inside unit circle
            sc_list.append(0)  # point's color will be cyan
            points_in_circle += 1
        else:
            sc_list.append(1)  # else point's color will be purple

        probability = points_in_circle / point_cumulative
        pi_approx_val = probability * 4
        pi_graph['x'].append(point_cumulative)
        pi_graph['y'].append(pi_approx_val)

    return sc_list, circle_graph, pi_graph


if __name__ == '__main__':

    sobol_points = generate_sobol()

    fig, (pseudo_ax, quasi_ax) = plt.subplots(2, 2)
    pseudo_circle, pseudo_graph = pseudo_ax

    quasi_circle, quasi_graph = quasi_ax

    pseudo_circle_line = pseudo_circle.scatter([], [],  # circle scatter plot
                                               marker=".", c=[],
                                               cmap='cool',
                                               vmin=0, vmax=1)  # 0: cyan, 1: purple
    pseudo_graph_line, = pseudo_graph.plot(
        [], [], 'g', linewidth=1.0)  # approx graph
    quasi_circle_line = quasi_circle.scatter([], [],  # circle scatter plot
                                             marker=".", c=[],
                                             cmap='cool',
                                             vmin=0, vmax=1)  # 0: cyan, 1: purple
    quasi_graph_line, = quasi_graph.plot(
        [], [], 'g', linewidth=1.0)  # approx graph
    ax = (pseudo_circle, pseudo_graph,
          quasi_circle, quasi_graph)
    line = (pseudo_circle_line, pseudo_graph_line,
            quasi_circle_line, quasi_graph_line)

    key_list = ['sc_list', 'circle_graph', 'pi_graph']

    pseudo_plot_detail = dict(
        zip(key_list, get_plot_details(func=pseudo_points)))
    quasi_plot_detail = dict(
        zip(key_list, get_plot_details(func=quasi_points, sobol=sobol_points)))

    graph = {'pseudo': pseudo_graph, 'quasi': quasi_graph}

    fargs = (pseudo_plot_detail, quasi_plot_detail, graph)
    ani = FuncAnimation(fig,
                        func=update_func,
                        fargs=fargs,
                        frames=np.linspace(0, POINTS, POINT_SPACING + 1),
                        init_func=lambda: init_plot(line, ax),
                        blit=False,
                        repeat=False,
                        interval=10)

    plt.rcParams.update({'font.size': 13, 'font.weight': 'bold'})
    plt.tight_layout()
    mng = plt.get_current_fig_manager()
    mng.window.showMaximized()
    plt.show()
