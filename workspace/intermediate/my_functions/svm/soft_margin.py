import numpy as np
from sklearn.svm import LinearSVC
from ipywidgets import interact, FloatLogSlider, fixed
import matplotlib.pyplot as plt
from matplotlib.figure import figaspect

resolution = 100


def plot(C, x, y):
    model = LinearSVC(C=C, random_state=1234, max_iter=int(1e6))
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
    ax.set(xticks=(), yticks=())
    plt.show()


def show(x, y):
    C = FloatLogSlider(value=0,
                       base=10,
                       min=-0.5,
                       max=3,
                       step=0.5,
                       description='$C$',
                       readout_format='.1f',
                       continuous_update=False)
    interact(plot, C=C, x=fixed(x), y=fixed(y))
