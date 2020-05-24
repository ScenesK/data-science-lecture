import numpy as np
from sklearn.svm import SVC
from ipywidgets import interact, Dropdown, FloatLogSlider, fixed
import matplotlib.pyplot as plt
from matplotlib.figure import figaspect

resolution = 100


def plot(kernel, C, gamma, fig, x, y):
    model = SVC(kernel=kernel, C=C, gamma=gamma, random_state=1234)
    model.fit(x, y)
    ax = fig.gca()
    ax.clear()
    ax.scatter(x[:, 0], x[:, 1], c=y, edgecolors='k')
    xlim = ax.get_xlim()
    ylim = ax.get_ylim()
    xx = np.linspace(xlim[0], xlim[1], resolution)
    yy = np.linspace(ylim[0], ylim[1], resolution)
    xx, yy = np.meshgrid(np.linspace(xlim[0], xlim[1], resolution),
                         np.linspace(ylim[0], ylim[1], resolution))
    grid = np.c_[xx.ravel(), yy.ravel()]
    ax.pcolormesh(xx,
                  yy,
                  model.predict(grid).reshape(xx.shape),
                  alpha=0.2,
                  edgecolors='none')
    ax.set(xticks=(), yticks=(), xlim=xlim, ylim=ylim)
    plt.show()


def show(x, y):
    kernel = Dropdown(options={
        '線形カーネル': 'linear',
        'ガウシアンカーネル': 'rbf'
    },
                      value='linear',
                      description='カーネル')
    C = FloatLogSlider(value=0,
                       base=10,
                       min=-1,
                       max=2,
                       step=1,
                       readout_format='.3f',
                       description='$C$',
                       continuous_update=False)
    gamma = FloatLogSlider(value=0,
                           base=10,
                           min=-3,
                           max=2,
                           step=0.5,
                           readout_format='.3f',
                           description='$\gamma$ (gamma)',
                           continuous_update=False)
    fig = plt.figure(figsize=figaspect(1))
    interact(plot,
             kernel=kernel,
             C=C,
             gamma=gamma,
             fig=fixed(fig),
             x=fixed(x),
             y=fixed(y))
