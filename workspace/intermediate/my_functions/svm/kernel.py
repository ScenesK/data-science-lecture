import numpy as np
from sklearn.svm import SVC
from ipywidgets import interact, FloatLogSlider, fixed
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from matplotlib.figure import figaspect

resolution = 50
fig = plt.figure(figsize=figaspect(1))
ax = plt.axes(projection='3d')


def plot(C, gamma, x, y):
    model = SVC(kernel='rbf', C=C, gamma=gamma, random_state=1234)
    model.fit(x, y)

    ax.clear()

    projection = model.decision_function(x)
    ax.scatter(x[:, 0], x[:, 1], projection, c=y, cmap='bwr')

    xlim, ylim = ax.get_xlim(), ax.get_ylim()
    xx, yy = np.meshgrid(np.linspace(xlim[0], xlim[1]),
                         np.linspace(ylim[0], ylim[1]))
    grid = np.c_[xx.ravel(), yy.ravel()]
    zz = model.decision_function(grid).reshape(xx.shape)
    ax.plot_surface(xx, yy, zz, alpha=0.5, cmap='bwr')

    ax.set(xticks=(), yticks=(), zticks=())
    plt.show()


def show(x, y):
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
                           description='$\gamma$',
                           continuous_update=False)
    interact(plot, C=C, gamma=gamma, x=fixed(x), y=fixed(y))
