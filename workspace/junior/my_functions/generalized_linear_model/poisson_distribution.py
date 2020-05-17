import numpy as np
from scipy.stats import poisson
import matplotlib.pyplot as plt
from matplotlib.figure import figaspect


def show():
    np.random.seed(1234)
    x = np.random.uniform(-3, 3, 200)
    y = poisson.rvs(np.exp(x))
    _, ax = plt.subplots(1, 1, figsize=figaspect(1))
    ax.scatter(x, y, s=4)
    ax.set(xlabel='$x$', ylabel='$y$', xticks=(), yticks=())
    plt.show()
