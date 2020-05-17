import numpy as np
from scipy.stats import norm
import matplotlib.pyplot as plt
from matplotlib.figure import figaspect
import seaborn as sns


def show():

    sample_size = 100
    categories = ['赤', '緑', '青']
    colors = ['r', 'g', 'b']
    n_category = len(categories)

    np.random.seed(1234)
    x = np.tile(np.arange(n_category).reshape(-1, 1), (1, sample_size))
    coef = np.random.normal(size=n_category)
    y = coef.reshape(-1, 1) + np.random.normal(size=(n_category, sample_size))
    hue = np.tile(np.array(['r', 'g', 'b']).reshape(-1, 1), (1, sample_size))

    _, ax = plt.subplots(1, 1, figsize=figaspect(1))
    sns.swarmplot(x.ravel(), y.ravel(), hue.ravel(), size=4, ax=ax)
    ax.legend().set_visible(False)
    collections = ax.collections
    for collection, color in zip(collections[:n_category], colors):
        collection.set_color(color)
    x_min, x_max = ax.get_xlim()
    ax.hlines(coef,
              x_min,
              np.arange(n_category),
              linestyle='dotted',
              alpha=0.3)
    ax.set(xlabel='$x$',
           ylabel='$y$',
           xlim=(x_min, x_max),
           xticklabels=categories,
           yticks=coef,
           yticklabels=['$a_{0}$', '$a_{0} +a_{1}$', '$a_{0} +a_{2}$'])
    plt.show()
