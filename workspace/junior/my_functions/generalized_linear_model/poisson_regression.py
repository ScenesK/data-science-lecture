import numpy as np
from scipy.stats import poisson
import matplotlib.pyplot as plt
from matplotlib.figure import figaspect


def show():

    resolution = 100
    x = np.linspace(0, np.log(5), 5)
    lambda_ = np.exp(x)

    np.random.seed(1234)
    y = poisson.rvs(lambda_)

    _, ax = plt.subplots(1, 1, figsize=figaspect(1))
    ax.scatter(x, y, c='k', label='$( x_{i} ,y_{i})$')
    x_min, x_max = ax.get_xlim()
    y_min, y_max = ax.get_ylim()
    ys = np.arange(0, y_max)
    yy = np.tile(ys.reshape(1, -1), (x.size, 1))
    xx = poisson.pmf(yy, lambda_.reshape(-1, 1))
    xx = (xx / xx.max()) * (x.max() / x.size) * 0.9
    xx += x.reshape(-1, 1)
    ax.hlines(yy,
              np.tile(x.reshape(-1, 1), (1, ys.size)),
              xx,
              color='b',
              label=r'$\mathcal{Poisson}\left( e^{z_{i}}\right)$')
    for i in x:
        ax.axvline(i, c='gray', linestyle='dotted', alpha=0.3)
    x_min, x_max = ax.get_xlim()
    xx = np.linspace(x_min, x_max, resolution)
    ax.plot(xx, np.exp(xx), c='k', label='$y=e^{z}$')
    ax.legend()
    ax.set(xlabel='$x$',
           ylabel='$y$',
           xlim=(x_min, x_max),
           ylim=(y_min, y_max))
    plt.show()
