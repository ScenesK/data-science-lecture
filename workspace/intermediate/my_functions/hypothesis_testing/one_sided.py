import numpy as np
from scipy import stats
from ipywidgets import interact, FloatSlider
import matplotlib.pyplot as plt
from matplotlib.figure import figaspect

x_min, x_max = -3, 3
resolution = 50


def plot(alpha):
    distribution = stats.norm()
    range_left, range_right = distribution.interval(1 - alpha * 2)
    left = np.linspace(x_min, range_left, resolution)
    center = np.linspace(range_left, range_right, resolution)
    right = np.linspace(range_right, x_max, resolution)
    _, axes = plt.subplots(1,
                           2,
                           figsize=figaspect(1 / 2),
                           sharex=True,
                           sharey=True)
    for i, ax in enumerate(axes):
        ax.fill_between(center,
                        distribution.pdf(center),
                        color='blue',
                        label='採択域')
        if i == 0:
            rejection = left
            title = '左側検定'
        else:
            rejection = right
            title = '右側検定'
        ax.fill_between(rejection,
                        distribution.pdf(rejection),
                        color='red',
                        label='棄却域')
        acception = -rejection
        ax.fill_between(acception, distribution.pdf(acception), color='blue')
        ax.legend()
        ax.set(title=title,
               xlim=(x_min, x_max),
               ylim=(0, ax.get_ylim()[1]),
               xticks=(),
               yticks=())
    plt.show()


def show():
    interact(plot,
             alpha=FloatSlider(value=0.05,
                               min=0.01,
                               max=0.3,
                               step=0.01,
                               description='有意水準',
                               continuous_update=False,
                               readout_format='.2f'))
