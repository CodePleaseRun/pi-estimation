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
    ax[0].set_title('Quasirandom Number Generation (Sobol Sequence)')

    ax[1].set_xlim(0, POINTS)
    ax[1].set(ylim=ylim)
    ax[1].set_xlabel('\nPoints Simulated', fontdict=font_dict)
    ax[1].set_ylabel('Estimated Value\n', fontdict=font_dict)
    ax[1].axhline(y=PI, color='r', linestyle='-')
    ax[1].legend(['Estimations', 'Value of π'])
    ax[0].set_xlim(0.001, 1)
    ax[0].set_ylim(0.001, 1)
    ax[0].axis('square')
    ax[0].set_xticks([])
    ax[0].set_yticks([])
    return line


def update_func(frame, quasi_plot_detail, graph):
    """
    Update the animation every frame
    - quasi_plot_details is a dict contaning 3 keys:
        `sc_list`: a color array for individual scatter plot point
        `circle_graph`: a dictionary with 'x', 'y' as key. Contains
                        coordinates for scatterplot
        `pi_graph`: a dictionary with 'x', 'y' as key. Contains
                        coordinates for pi graph

    - graph: Axes for quasi pi graph
            Used for updaing the title of pi graph

    """
    frame = int(frame+1)
    quasi_sc_list = quasi_plot_detail['sc_list']
    quasi_circle_graph = quasi_plot_detail['circle_graph']
    quasi_pi_graph = quasi_plot_detail['pi_graph']
    quasi_graph_ax = graph
    quasi_pg_x = quasi_pi_graph['x'][:frame]
    quasi_pg_y = quasi_pi_graph['y'][:frame]
    quasi_cg_x = quasi_circle_graph['x'][:frame]
    quasi_cg_y = quasi_circle_graph['y'][:frame]
    quasi_pi = quasi_pg_y[-1]
    quasi_title = f'π estimate = {quasi_pi:4f}   Error = {abs((PI - quasi_pi)):4f}'
    quasi_graph_ax.set_title(quasi_title)
    # setting sactter plot coordinates for quasi graph
    line[0].set_offsets(np.c_[quasi_cg_x, quasi_cg_y])
    # setting color array for quasi scatter plot
    line[0].set_array(quasi_sc_list[:frame])
    # setting quasi pi approx graph coordinates
    line[1].set_data(quasi_pg_x, quasi_pg_y)
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
    fig, quasi_ax = plt.subplots(1, 2)
    quasi_circle, quasi_graph = quasi_ax
    quasi_circle_line = quasi_circle.scatter([], [],  # circle scatter plot
                                             marker=".", c=[],
                                             cmap='cool',
                                             vmin=0, vmax=1)  # 0: cyan, 1: purple
    quasi_graph_line, = quasi_graph.plot(
        [], [], 'g', linewidth=1.0)  # approx graph
    ax = (quasi_circle, quasi_graph)
    line = (quasi_circle_line, quasi_graph_line)
    key_list = ['sc_list', 'circle_graph', 'pi_graph']
    quasi_plot_detail = dict(
        zip(key_list, get_plot_details(func=quasi_points, sobol=sobol_points)))
    graph = quasi_graph
    fargs = (quasi_plot_detail, graph)
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
