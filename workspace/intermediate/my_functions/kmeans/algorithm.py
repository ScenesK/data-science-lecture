import numpy as np
from sklearn.datasets import make_blobs
from sklearn.cluster import KMeans
from ipywidgets import interactive_output, IntSlider, Play, jslink
import matplotlib.pyplot as plt
from matplotlib.figure import figaspect
import seaborn as sns
from IPython.display import display

n_clusters = 3
max_iter = 5
centers = [(np.cos(np.pi * 2 / n_clusters * i),
            np.sin(np.pi * 2 / n_clusters * i)) for i in range(n_clusters)]
X, _ = make_blobs(n_samples=100,
                  centers=centers,
                  cluster_std=0.3,
                  shuffle=False,
                  random_state=1234)
resolution = 100
models = []
history = np.empty((max_iter + 1, n_clusters, 2))

init = np.array([((centers[i][0] + centers[(i + 1) % n_clusters][0]) / 2,
                  (centers[i][1] + centers[(i + 1) % n_clusters][1]) / 2)
                 for i in range(n_clusters)])
kwargs = dict(n_clusters=n_clusters, n_init=1, max_iter=1)
for i in range(max_iter + 1):
    if i == 0:
        model = KMeans(init=init, **kwargs)
    else:
        model = KMeans(init=history[i - 1], **kwargs)
    model.fit(X)
    models.append(model)
    history[i] = model.cluster_centers_
colors = np.array(sns.color_palette(n_colors=n_clusters))

n_scenes = 4


def plot(i):
    step = i // n_scenes
    scene = i % n_scenes
    model = models[step]
    cluster_centers = history[step]
    fig = plt.figure(figsize=figaspect(1))
    ax = fig.gca()

    def _get_lim():
        return np.max([np.abs(ax.get_xlim()), np.abs(ax.get_ylim())])

    def _plot_sample(color='gray', alpha=0.2):
        ax.scatter(X[:, 0], X[:, 1], color=color, alpha=alpha)
        lim = _get_lim()
        ax.set(xlim=(-lim, lim), ylim=(-lim, lim), xticks=(), yticks=())

    def _plot_center(cluster_centers, alpha=1.):
        ax.scatter(cluster_centers[:, 0],
                   cluster_centers[:, 1],
                   color=colors,
                   alpha=alpha,
                   marker='x')

    if scene == 0:
        _plot_sample()
        _plot_center(cluster_centers)
    elif scene == 1:
        _plot_sample()
        _plot_center(cluster_centers)
        lim = _get_lim()
        xx, yy = np.meshgrid(np.linspace(-lim, lim, resolution),
                             np.linspace(-lim, lim, resolution))
        grid = np.c_[xx.ravel(), yy.ravel()]
        ax.scatter(xx.ravel(),
                   yy.ravel(),
                   c=colors[model.predict(grid)],
                   marker='.',
                   alpha=0.05,
                   edgecolors='none')
    elif scene == 2:
        _plot_sample(color=colors[model.predict(X)], alpha=0.7)
        _plot_center(cluster_centers, alpha=0.4)
    else:
        prediction = model.predict(X)
        _plot_sample(color=colors[prediction])
        _plot_center(cluster_centers, alpha=0.2)
        new_centers = history[step + 1]
        _plot_center(new_centers)
        for idx, (x, y) in enumerate(X):
            label = prediction[idx]
            ax.plot((x, new_centers[label, 0]), (y, new_centers[label, 1]),
                    color=colors[label],
                    alpha=0.2)
    plt.show()


def show():
    max_ = max_iter * n_scenes
    i = IntSlider(value=0, min=0, max=max_, continuous_update=False)
    play = Play(interval=2000, value=0, min=0, max=max_, step=1)
    jslink((play, 'value'), (i, 'value'))
    output = interactive_output(plot, dict(i=i))
    display(play, output)
