import pandas as pd
from sklearn.datasets import load_iris
from sklearn.tree import DecisionTreeClassifier, plot_tree, export_text
from ipywidgets import interactive_output, IntSlider, Play, jslink
import matplotlib.pyplot as plt
from matplotlib.figure import figaspect
import seaborn as sns
from IPython.display import display

data = sns.load_dataset('iris')
data['species'] = pd.Categorical(data['species'])
X = data.iloc[:, :-1]
y = data.iloc[:, -1]


def plot(depth):
    model = DecisionTreeClassifier(max_depth=depth).fit(X, y)
    fig = plt.figure(figsize=figaspect(1.5 / 2) * depth)
    ax = fig.gca()
    plot_tree(model,
              feature_names=X.columns,
              class_names=y.cat.categories,
              filled=True,
              impurity=False,
              ax=ax,
              fontsize='large')
    plt.show()
    print(export_text(model, feature_names=X.columns.tolist()))


def show():
    max_depth = 5
    depth = IntSlider(value=1, min=1, max=max_depth, continuous_update=False)
    play = Play(interval=1000, value=1, min=1, max=max_depth, step=1)
    jslink((play, 'value'), (depth, 'value'))
    output = interactive_output(plot, dict(depth=depth))
    display(play, output)
