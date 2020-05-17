import numpy as np
import matplotlib.pyplot as plt
from matplotlib.figure import figaspect


def show():
    np.random.seed(1234)
    a = np.random.uniform(size=4)

    y = np.full(4, a[0])
    yticklabels = ['a_{0}'] * 4
    for x1, x2 in np.ndindex((2, 2)):
        i = x1 + x2 * 2
        if x1:
            y[i] += a[1]
            yticklabels[i] += '+a_{1}'
        if x2:
            y[i] += a[2]
            yticklabels[i] += '+a_{2}'
    y[-1] += a[-1]
    yticklabels[-1] += '+a_{3}'

    sum_naive = a[:-1].sum()
    _, ax = plt.subplots(1, 1, figsize=figaspect(1))

    xticklabels = ['なし', '喫煙のみ', '飲酒のみ', '喫煙+飲酒']
    yticks = list(y) + [sum_naive]
    yticklabels.append('+'.join([f'a_{{{i}}}' for i in range(3)]))
    yticklabels = [f'${l}$' for l in yticklabels]

    ax.bar(np.arange(4), y)
    ax.bar(3, a[-1], bottom=sum_naive, label='交互作用')

    for tick in yticks:
        ax.axhline(tick, color='gray', linestyle='dotted')

    ax.legend()
    ax.set(xticks=np.arange(4),
           yticks=yticks,
           xticklabels=xticklabels,
           yticklabels=yticklabels)
    plt.show()
