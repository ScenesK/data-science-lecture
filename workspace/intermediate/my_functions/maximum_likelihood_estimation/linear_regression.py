import numpy as np
from scipy.stats import norm
import matplotlib.pyplot as plt
from matplotlib.figure import figaspect


def show():

    x_min, x_max = -3, 3
    coef = 2
    sigma = 1
    x = np.arange(x_min + 1, x_max)

    np.random.seed(1234)
    e = np.random.normal(scale=sigma, size=x.size)

    fig = plt.figure(figsize=figaspect(1))
    ax = fig.gca()
    ax.plot((x_min, x_max), (x_min * coef, x_max * coef),
            c='k',
            label='$f(X_{i})$')
    ax.scatter(x, x * coef + e, c='k', label='$(X_{i},\ y_{i})$')
    for i, y_hat in enumerate(x * coef):
        x_tmp = x_min + i + 1
        ee = np.linspace(-sigma * 3, sigma * 3, 10)
        xx = x_tmp + norm.pdf(ee)
        yy = y_hat + ee
        lines = ax.plot(xx, yy, c='b')
        line_collection = ax.hlines(y_hat + e[i],
                                    x_tmp,
                                    x_tmp + norm.pdf(e[i]),
                                    color='r')
        if i == 0:
            lines[0].set(label=r'$\epsilon _{i}$')
            line_collection.set(label=r'$P(y_{i}\ |\ X_{i})$')
    ax.legend()
    ax.set(xlim=(x_min, x_max), xticks=(), yticks=())
    plt.show()
