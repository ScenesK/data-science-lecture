import numpy as np
from scipy.stats import binom
import matplotlib.pyplot as plt
from matplotlib.figure import figaspect


def show(n):
    np.random.seed(1234)
    x = np.random.uniform(-5, 5, 100)
    p = 1 / (1 + np.exp(-x))
    y = binom.rvs(n, p)
    _, ax = plt.subplots(1, 1, figsize=figaspect(1))
    ax.scatter(x, y, s=4)
    ax.set(xlabel='$x$', ylabel='$y$', xticks=(), yticks=())
    plt.show()
