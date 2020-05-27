from collections import defaultdict
import numpy as np
from sklearn.datasets import make_blobs
from sklearn.cluster._mean_shift import estimate_bandwidth
from ipywidgets import interactive_output, IntSlider, Play, jslink
import matplotlib.pyplot as plt
from matplotlib.figure import figaspect
from matplotlib.patches import Circle

min_bin_freq = 1
X, _ = make_blobs(centers=3,
                  cluster_std=1,
                  center_box=(-7, 7),
                  shuffle=False,
                  random_state=1234)
bandwidth = estimate_bandwidth(X, n_jobs=-1)

bin_sizes = defaultdict(int)
for point in X:
    binned_point = np.round(point / bandwidth)
    bin_sizes[tuple(binned_point)] += 1

lowers = np.round(X.min(axis=0) / bandwidth)
uppers = np.round(X.max(axis=0) / bandwidth)
xbounds = np.arange(lowers[0] + 0.5, uppers[0] + 1.5) * bandwidth
ybounds = np.arange(lowers[1] + 0.5, uppers[1] + 1.5) * bandwidth

bin_seeds = np.array(
    [point for point, freq in bin_sizes.items() if freq >= min_bin_freq],
    dtype=np.float32) * bandwidth


def _get_neighbors(point):
    return X[np.sqrt(np.sum((X - point)**2, axis=1)) <= bandwidth]


history = []
for center in bin_seeds:
    movement = [center]
    while True:
        neighbors = _get_neighbors(center)
        new_center = neighbors.mean(axis=0)
        movement.append(new_center)
        if np.allclose(movement[-2], new_center, rtol=0,
                       atol=bandwidth * 0.01):
            break
        center = new_center
    history.append(movement)

n_intro = 2
n_scenes = 4


def plot(i):
    fig = plt.figure(figsize=figaspect(1))
    ax = fig.gca()
    ax.scatter(X[:, 0], X[:, 1], color='gray', alpha=0.2)
    xlim, ylim = ax.get_xlim(), ax.get_ylim()

    def _plot_centers(x, y, alpha=1):
        ax.scatter(x, y, color='red', alpha=alpha, marker='x')

    if i == 0:
        pass
    elif i == 1:
        ax.vlines(xbounds, ylim[0], ylim[1], alpha=0.2)
        ax.hlines(ybounds, xlim[0], xlim[1], alpha=0.2)
        _plot_centers(bin_seeds[:, 0], bin_seeds[:, 1], alpha=0.2)
    else:
        j = i - n_intro
        order = -1
        scene = j % n_scenes
        while j >= 0:
            order += 1
            step = j // n_scenes
            j -= (len(history[order]) - 1) * n_scenes

        if order > 0:
            formers = np.array([history[i][-1] for i in range(order)])
            _plot_centers(formers[:, 0], formers[:, 1])
        if order < len(history) - 1:
            _plot_centers(bin_seeds[order + 1:, 0],
                          bin_seeds[order + 1:, 1],
                          alpha=0.2)
        movement = history[order]
        center = movement[step]
        center_x, center_y = center[0], center[1]
        if scene == 0:
            _plot_centers(center_x, center_y)
            ax.add_patch(
                Circle((center_x, center_y),
                       radius=bandwidth,
                       fill=False,
                       edgecolor='red'))
        else:
            if scene < 3:
                _plot_centers(center_x, center_y, alpha=0.2)
            neighbors = _get_neighbors((center_x, center_y))
            if scene == 1:
                ax.scatter(neighbors[:, 0], neighbors[:, 1], color='red')
            else:
                new_x, new_y = movement[step + 1]
                if scene == 2:
                    ax.scatter(neighbors[:, 0],
                               neighbors[:, 1],
                               color='red',
                               alpha=0.2)
                    _plot_centers(new_x, new_y)
                    for x, y in neighbors:
                        ax.plot((x, new_x), (y, new_y), color='red', alpha=0.2)
                else:
                    _plot_centers(new_x, new_y)
    ax.set(xlim=xlim,
           ylim=ylim,
           xticks=(),
           yticks=(),
           xticklabels=(),
           yticklabels=())
    plt.show()


def show():
    max_ = sum([(len(movement) - 1) * n_scenes
                for movement in history]) + n_intro - 1
    i = IntSlider(value=0, min=0, max=max_, continuous_update=False)
    play = Play(interval=1000, value=0, min=0, max=max_, step=1)
    jslink((play, 'value'), (i, 'value'))
    output = interactive_output(plot, dict(i=i))
    display(play, output)
