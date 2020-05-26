import numpy as np
from scipy import stats
import statsmodels.api as sm
import matplotlib.pyplot as plt
from matplotlib.figure import figaspect


def show():
    p = np.linspace(0.01, 0.99, 20)
    y = stats.expon.ppf(p)
    _, ax = plt.subplots(figsize=figaspect(1))
    sm.qqplot(y, stats.norm, line='s', ax=ax)
    ax.set(xlabel='正規分布の分位点', ylabel='指数分布の分位点')
    plt.show()
