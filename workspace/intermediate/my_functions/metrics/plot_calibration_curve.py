from sklearn.datasets import make_classification
from sklearn.linear_model import LogisticRegression
from sklearn.calibration import calibration_curve
import matplotlib.pyplot as plt
from matplotlib.figure import figaspect


def show():
    x, y = make_classification(n_samples=500, random_state=1234)
    model = LogisticRegression().fit(x, y)
    y_hat = model.predict_proba(x)[:, 1]
    yy, xx = calibration_curve(y, y_hat, n_bins=10)
    _, ax = plt.subplots(1, 1, figsize=figaspect(1))
    ax.plot(xx, yy, marker='o')
    ax.plot([0, 1], [0, 1], color='gray', linestyle='dashed', label='理想的な状態')
    ax.legend()
    ax.set(title='calibration curve')
    plt.show()
