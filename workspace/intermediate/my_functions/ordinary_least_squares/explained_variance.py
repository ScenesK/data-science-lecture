import numpy as np
from scipy import stats
import statsmodels.api as sm
from ipywidgets import interact, IntSlider, FloatSlider
import matplotlib.pyplot as plt
from matplotlib.figure import figaspect


def plot(r, random_seed):
    n = 100
    slope = 2
    np.random.seed(random_seed)
    x = np.random.uniform(size=n)
    e = np.random.uniform(size=n)
    y = r * x + np.sqrt(1 - r**2) * e
    y *= slope

    X = sm.add_constant(x)
    result = sm.OLS(y, X).fit()
    coef = result.params[1]
    print('回帰係数 : {:.2f}'.format(coef))
    print('R^2 : {:.3f}'.format(result.rsquared))

    fig = plt.figure(figsize=figaspect(slope))
    ax = fig.gca()
    ax.scatter(x - x.mean(), y - y.mean(), marker='.')
    xmin, xmax = ax.get_xlim()
    ymin, ymax = ax.get_ylim()
    ax.plot((xmin, xmax), (coef * xmin, coef * xmax), c='black')
    kwargs = dict(linestyles='dotted', alpha=0.4)
    ax.hlines(0, xmin, 0, **kwargs)
    ax.vlines(0, ymin, 0, **kwargs)
    x_sample = xmax / 2
    y_hat = coef * x_sample
    y_sample = y_hat + np.sqrt(1 - r**2) * np.random.uniform(size=1)
    ax.scatter(x_sample, y_sample, c='red')
    ax.hlines(0, 0, x_sample, color='green', **kwargs)
    ax.vlines(x_sample, 0, y_hat, color='green', **kwargs)
    ax.hlines(y_hat, 0, x_sample, **kwargs)
    ax.vlines(x_sample, y_hat, y_sample, color='orange', **kwargs)
    ax.hlines(y_sample, 0, x_sample, color='orange', **kwargs)
    kwargs = dict(linestyles='solid')
    ax.vlines(0, 0, y_hat, color='green', label='回帰方程式で説明できる部分', **kwargs)
    ax.vlines(0,
              y_hat,
              y_sample,
              color='orange',
              label='回帰方程式で説明できない部分',
              **kwargs)

    ax.legend(loc='lower left')
    ax.set(xlim=(xmin, xmax),
           ylim=(ymin, ymax),
           xticks=(0, ),
           yticks=(0, ),
           xticklabels=(r'$\bar{x}$', ),
           yticklabels=(r'$\bar{y}$', ))

    plt.show()


def show():
    style = dict(description_width='7em')
    r = FloatSlider(value=0.8,
                    min=0.1,
                    max=1,
                    step=0.1,
                    description='相関係数 (目安)',
                    continuous_update=False,
                    readout_format='.1f',
                    style=style)
    seed = IntSlider(value=1,
                     min=1,
                     max=256,
                     description='乱数',
                     continuous_update=False,
                     style=style)
    interact(plot, r=r, random_seed=seed)
