import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

from .acquisition import AcquisitionFunction
from .bounds import Bound
from .surrogate import Surrogate

sns.set_style("darkgrid")

__all__ = ["plot_surrogate_1D", "plot_acquisition_function_1D"]


def plot_surrogate_1D(
    ax: plt.Axes,
    surrogate: Surrogate,
    x_train: np.ndarray,
    y_train: np.ndarray,
    bound: Bound,
    n_points: int = 100,
) -> None:
    """Plot a 1D surrogate model.

    Parameters
    ----------
    ax: plt.Axes
        matplotlib axes object on which
        to plot the graph.
    surrogate: Surrogate
        A trained surrogate model.
    x_train: np.ndarray of shape (n_samples, 1)
        The training inputs on which
        the surrogate was trained.
    y_train: np.ndarray of shape (n_samples,)
        The training targets on which
        the surrogate was trained.
    bound: Bound
        The bound on which to plot
        the graph. NB: doesn't have to be
        the same as the optimization bound.
    n_points: int (default = 100)
        The number of points with with
        to plot the graph.
    """
    x = np.linspace(bound.lower, bound.upper, n_points).reshape(-1, 1)
    y_pred, sigma = surrogate.predict(x)
    std = np.sqrt(np.diag(sigma))
    lower = y_pred - 2 * std
    upper = y_pred + 2 * std

    ax.plot(x.flatten(), y_pred, label="mean")
    ax.fill_between(x.flatten(), lower, upper, alpha=0.5, label="confidence interval")
    ax.plot(x_train.flatten(), y_train, "k+", label="training data")


def plot_acquisition_function_1D(
    ax: plt.Axes,
    acquisition_function: AcquisitionFunction,
    surrogate: Surrogate,
    bound: Bound,
    n_points: int = 100,
) -> None:
    """Plot a 1D acquisition_function.

    Parameters
    ----------
    ax: plt.Axes
        matplotlib axes object on which
        to plot the graph.
    acquisition_function: AcquisitionFunction
        A trained acquisition function.
    surrogate: Surrogate
        A trained surrogate model.
    bound: Bound
        The bound on which to plot
        the graph. NB: doesn't have to be
        the same as the optimization bound.
    n_points: int (default = 100)
        The number of points with with
        to plot the graph.
    """
    x = np.linspace(bound.lower, bound.upper, n_points).reshape(-1, 1)
    a_x = acquisition_function(surrogate, x)

    ax.plot(x.flatten(), a_x, label="acquisition function")