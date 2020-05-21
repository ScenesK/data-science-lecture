import numpy as np
from sklearn.cluster import KMeans
from ipywidgets import interact, IntSlider, fixed
import matplotlib.pyplot as plt
from matplotlib.figure import figaspect
from matplotlib.patches import Patch
import seaborn as sns

resolution = 200


def plot(k, df):
    x = df.values
    model = KMeans(n_clusters=k, random_state=1)
    model.fit(x)
    plt.figure(figsize=figaspect(1))
    ax = plt.axes()
    df.plot.scatter(df.columns[0],
                    df.columns[1],
                    c='black',
                    s=10,
                    label='元のデータ',
                    ax=ax)
    xlim, ylim = ax.get_xlim(), ax.get_ylim()
    xx, yy = np.meshgrid(np.linspace(xlim[0], xlim[1], resolution),
                         np.linspace(ylim[0], ylim[1], resolution))
    grid = np.c_[xx.ravel(), yy.ravel()]
    pred = model.predict(grid)
    palette = sns.color_palette()
    ax.scatter(xx,
               yy,
               c=[palette[i] for i in pred],
               marker='.',
               alpha=0.2,
               edgecolors='none')
    centers = model.cluster_centers_
    ax.scatter(centers[:, 0],
               centers[:, 1],
               marker='x',
               s=100,
               c='blue',
               label='クラスタ中心')
    handles, labels = ax.get_legend_handles_labels()
    handles.extend([Patch(color=palette[i]) for i in range(k)])
    labels.extend([f'クラスタ{i + 1}' for i in range(k)])
    ax.legend(handles, labels)
    ax.set(xlim=xlim, ylim=ylim, xticks=(), yticks=())
    plt.show()


def show(df):
    k = IntSlider(value=3, min=2, max=5, continuous_update=False)
    interact(plot, k=k, df=fixed(df))
