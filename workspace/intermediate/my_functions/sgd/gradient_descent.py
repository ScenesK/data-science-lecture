import numpy as np
from sklearn.datasets import make_regression
from tensorflow.keras import backend as K
from tensorflow.keras.initializers import Constant
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.optimizers import SGD
from tensorflow.keras.callbacks import Callback


def get_data(n, dim):
    return make_regression(n_samples=n,
                           n_features=dim,
                           n_informative=dim,
                           coef=True,
                           random_state=1234)


def get_costs(W, X, y):
    return (((y - W.dot(X.T))**2).mean(axis=1))


def train(coef, X, y, lr=0.3, batch_size=None, epochs=5, init_w=0.9):
    n = y.size
    if batch_size is None:
        batch_size = n

    class TrainHistory(Callback):
        def on_train_begin(self, logs={}):
            self.weights = []
            self.losses = []

        def on_epoch_begin(self, epoch, logs={}):
            pass

        def on_batch_begin(self, batch, logs={}):
            self._get_weights()
            self._get_total_loss()

        def on_epoch_end(self, epoch, logs={}):
            pass

        def on_train_end(self, epoch, logs={}):
            self._get_weights()
            self._get_total_loss()

        def _get_weights(self):
            self.weights.append(model.layers[0].get_weights()[0].ravel())

        def _get_total_loss(self):
            self.losses.append(model.evaluate(X, y, batch_size=n, verbose=0))

    init = Constant(coef + init_w)
    hist = TrainHistory()
    K.clear_session()
    model = Sequential([
        Dense(1, use_bias=False, kernel_initializer=init, input_dim=X.shape[1])
    ])
    model.compile(optimizer=SGD(lr=lr), loss='mean_squared_error')
    model.fit(X,
              y,
              batch_size=batch_size,
              epochs=epochs,
              verbose=0,
              callbacks=[hist])

    return np.array(hist.weights), np.array(hist.losses)
