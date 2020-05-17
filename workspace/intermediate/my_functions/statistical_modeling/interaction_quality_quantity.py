import numpy as np
import matplotlib.pyplot as plt
from matplotlib.figure import figaspect


def show():
    size = 3
    x = np.array([1, 2])

    np.random.seed(1234)
    a = np.random.uniform(high=2, size=size).cumsum()
    b = np.random.uniform(size=size)

    _, ax = plt.subplots(1, 1, figsize=figaspect(1))
    for slope, intercept, label in zip(a, b, ['40代', '30代', '20代']):
        y = slope * x + intercept
        ax.plot(x, y, label=label)
    ax.legend()
    ax.set(xlabel='$x_{1}$', ylabel='$y$', xlim=x, xticks=(), yticks=())
    plt.show()
