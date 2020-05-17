import numpy as np
from scipy.stats import norm
import matplotlib.pyplot as plt
from matplotlib.figure import figaspect


def show():

    resolution = 100
    x_min, x_max = -3, 3
    coef = 2
    sigma = 1
    x = np.arange(x_min + 1, x_max)

    np.random.seed(1234)
    e = np.random.normal(scale=sigma, size=x.size)

    _, ax = plt.subplots(1, 1, figsize=figaspect(1))
    ax.plot((x_min, x_max), (x_min * coef, x_max * coef),
            c='k',
            label=r'$y=a_{0} +a_{1} x$')
    ax.scatter(x, x * coef + e, c='k', label='$( x_{i} ,y_{i})$')
    ee = np.linspace(-sigma * 3, sigma * 3, resolution)
    xx = x.reshape(1, -1) + norm.pdf(ee).reshape(-1, 1)
    y_hat = x * coef
    yy = y_hat.reshape(1, -1) + ee.reshape(-1, 1)
    lines = ax.plot(xx, yy, c='b')
    lines[0].set(label=r'$\mathcal{N}\left( z_{i} ,\sigma ^{2}\right)$')
    ax.legend()
    ax.set(xlabel='$x$',
           ylabel='$y$',
           xlim=(x_min, x_max),
           xticks=(),
           yticks=())
    plt.show()