import numpy as np
from scipy.stats import binom
import matplotlib.pyplot as plt
from matplotlib.figure import figaspect


def sigmoid(x):
    return 1 / (1 + np.exp(-x))


def show():

    resolution = 100

    np.random.seed(1234)

    x = np.arange(-2, 3)
    n = 10
    p = sigmoid(x)
    y = binom.rvs(n, p)

    _, ax = plt.subplots(1, 1, figsize=figaspect(1))
    ax.scatter(x, y, c='k', label='$( x_{i} ,y_{i})$')
    ys = np.arange(0, n + 1)
    yy = np.tile(ys.reshape(1, -1), (x.size, 1))
    xx = binom.pmf(yy, n, p.reshape(-1, 1))
    xx = (xx / xx.max()) * 0.9
    xx += x.reshape(-1, 1)
    ax.hlines(
        yy,
        np.tile(x.reshape(-1, 1), (1, ys.size)),
        xx,
        color='b',
        label=r'$y_{i} \sim \mathcal{B}\left( n,\frac{1}{1+e^{-z_{i}}}\right)$'
    )
    for i in x:
        ax.axvline(i, color='gray', linestyle='dotted', alpha=0.3)
    x_min, _ = ax.get_xlim()
    x_max = x.max() + 1
    xx = np.linspace(x_min, x_max, resolution)
    ax.plot(xx,
            n * sigmoid(xx),
            c='k',
            label=r'$y=n\times \frac{1}{1+e^{-x}}$')
    ax.legend()
    ax.set(xlabel='$x$',
           ylabel='$y$',
           xlim=(x_min, x_max),
           yticks=(0, n),
           yticklabels=(0, 'n'))
    plt.show()