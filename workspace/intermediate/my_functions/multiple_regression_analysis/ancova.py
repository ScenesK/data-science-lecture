import numpy as np
import matplotlib.pyplot as plt
from matplotlib.figure import figaspect


def show():

    sample_size = 100
    scale = 2
    categories = ['赤', '緑', '青']
    colors = ['r', 'g', 'b']
    n_category = len(categories)

    np.random.seed(1234)
    x = np.random.uniform(size=(n_category, sample_size))
    slope = scale * 5
    intercept = np.random.normal(scale=scale, size=n_category)
    noise = np.random.normal(size=(n_category, sample_size))
    y = intercept.reshape(-1, 1) + x * slope + noise
    c = np.tile(np.array(['r', 'g', 'b']).reshape(-1, 1), (1, sample_size))

    _, ax = plt.subplots(1, 1, figsize=figaspect(1))
    ax.scatter(x.ravel(), y.ravel(), c=c.ravel(), alpha=0.3)
    xlim = np.array(ax.get_xlim())
    ylim = np.array(ax.get_ylim())
    for i in range(n_category):
        ax.plot(
            xlim,
            xlim * slope + intercept[i],
            c=colors[i],
        )
    ax.set(xlabel='$x_{2}$',
           ylabel='$y$',
           xlim=xlim,
           ylim=ylim,
           xticks=(),
           yticks=())
    plt.show()
