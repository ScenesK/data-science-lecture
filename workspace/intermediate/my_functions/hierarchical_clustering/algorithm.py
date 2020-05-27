import numpy as np
from scipy.spatial.distance import pdist, squareform
from sklearn.datasets import make_blobs
from ipywidgets import interactive_output, IntSlider, Play, jslink
import matplotlib.pyplot as plt
from matplotlib.figure import figaspect
import seaborn as sns
from IPython.display import display

n_samples = 10
X, _ = make_blobs(n_samples=n_samples,
                  centers=3,
                  shuffle=False,
                  random_state=1234)
history = [X]
centroids = X
children = {tuple(p): [p] for p in X}
while len(centroids) > 1:
    size = len(centroids)
    dist_matrix = squareform(pdist(centroids))
    dist_matrix += np.eye(size) * dist_matrix.max() * 2
    nearests = np.unravel_index(np.argmin(dist_matrix), (size, size))
    new_children = np.vstack([
        children[tuple(centroids[nearests[0]])],
        children[tuple(centroids[nearests[1]])]
    ])
    new_centroid = new_children.mean(axis=0)
    children[tuple(new_centroid)] = new_children
    centroids = np.array(
        [new_centroid] +
        [c for i, c in enumerate(centroids) if i not in nearests])
    history.append(centroids)

centroids_unique = set()
for centroids in history:
    for centroid in centroids:
        centroids_unique.add(tuple(centroid))
centroids_unique = sorted(list(centroids_unique))

colors = sns.color_palette(n_colors=len(centroids_unique))

n_scenes = 3


def plot(i):
    fig = plt.figure(figsize=figaspect(1))
    ax = fig.gca()
    lim = np.abs(X).max() + 1
    ax.set(title='セントロイド法',
           xlim=(-lim, lim),
           ylim=(-lim, lim),
           xticks=(),
           yticks=())
    step = i // n_scenes
    scene = i % n_scenes
    centroids = history[step]

    def plot_parents(ax, centroids):
        ax.scatter(centroids[:, 0],
                   centroids[:, 1],
                   color=[
                       colors[centroids_unique.index(tuple(p))]
                       for p in centroids
                   ])

    def plot_children(ax, centroids):
        for centroid in centroids:
            points = np.array([c for c in children[tuple(centroid)]])
            ax.scatter(points[:, 0],
                       points[:, 1],
                       color=colors[centroids_unique.index(tuple(centroid))],
                       alpha=0.2)

    if scene == 0:
        plot_parents(ax, centroids)
        plot_children(ax, centroids)
    else:
        new_centroids = history[step + 1]
        nearest_points = np.array(
            [c for c in centroids if c not in new_centroids])
        if scene == 1:
            plot_parents(ax, centroids)
            plot_children(ax, centroids)
            plot_parents(ax, nearest_points)
            ax.plot(nearest_points[:, 0], nearest_points[:, 1], color='red')
        else:
            plot_parents(ax, new_centroids)
            plot_children(ax, centroids)
            new_centroid = [c for c in new_centroids if c not in centroids][0]
            for point in children[tuple(new_centroid)]:
                ax.plot((new_centroid[0], point[0]),
                        (new_centroid[1], point[1]),
                        color='red',
                        alpha=0.2)
    plt.show()


def show():
    max_ = (len(history) - 1) * n_scenes
    i = IntSlider(value=0, min=0, max=max_, continuous_update=False)
    play = Play(interval=1000, value=0, min=0, max=max_, step=1)
    jslink((play, 'value'), (i, 'value'))
    output = interactive_output(plot, dict(i=i))
    display(play, output)
