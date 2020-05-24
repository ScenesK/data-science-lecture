import numpy as np
from sklearn.svm import LinearSVC
import matplotlib.pyplot as plt
from matplotlib.figure import figaspect

resolution = 100


def show(x, y):
    model = LinearSVC(C=1e30, random_state=1234)
    model.fit(x, y)

    fig = plt.figure(figsize=figaspect(1))
    ax = fig.gca()
    ax.scatter(x[:, 0], x[:, 1], c=y)

    xlim = ax.get_xlim()
    ylim = ax.get_ylim()
    xx, yy = np.meshgrid(np.linspace(xlim[0], xlim[1], resolution),
                         np.linspace(ylim[0], ylim[1], resolution))
    grid = np.c_[xx.ravel(), yy.ravel()]
    zz = model.decision_function(grid).reshape(xx.shape)
    cs = ax.contour(xx,
                    yy,
                    zz,
                    colors='k',
                    levels=[-1, 0, 1],
                    linewidths=0.8,
                    linestyles=['--', '-', '--'])
    fmt = {
        c: '決定境界' if i == 1 else 'サポートベクトル'
        for i, c in enumerate(cs.levels)
    }
    ax.clabel(cs, fontsize='large', fmt=fmt)

    ax.set(xlim=xlim, ylim=ylim, xticks=(), yticks=())
    plt.show()
