from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Tuple

import numpy as np
from DIRECT import solve

from .acquisition import AcquisitionFunction
from .bounds import Bounds
from .surrogate import Surrogate


@dataclass
class OptimizationResult:
    """Optimization result.

    Parameters
    ----------
    x_min: np.ndarray of shape (n_dimensions,)
        The argmin.
    f_min: float
        The min.
    """

    x_min: np.ndarray
    f_min: float


class Optimizer(ABC):
    """An acquisition function Optimizer.

    Optimizers find the minimum of a given
    acquisition function. This minimum is
    then used as the next query location
    of the objective function.

    This class shouldn't be used directly, use a derived class instead.
    """

    def optimize(
        self,
        acquisition_function: AcquisitionFunction,
        surrogate: Surrogate,
        bounds: Bounds,
    ) -> OptimizationResult:
        x_min, f_min = self._optimize(acquisition_function, surrogate, bounds)
        return OptimizationResult(x_min=x_min, f_min=f_min)

    @abstractmethod
    def _optimize(
        self,
        acquisition_function: AcquisitionFunction,
        surrogate: Surrogate,
        bounds: Bounds,
    ) -> Tuple[np.ndarray, float]:
        raise NotImplementedError


class DirectOptimizer(Optimizer):
    def __init__(self, *direct_args, **direct_kwargs):
        self.direct_args = direct_args
        self.direct_kwargs = direct_kwargs

    def _optimize(
        self,
        acquisition_function: AcquisitionFunction,
        surrogate: Surrogate,
        bounds: Bounds,
    ) -> Tuple[np.ndarray, float]:
        def wrapped_f(x, _):
            return acquisition_function(surrogate, x.reshape(1, -1)), 0

        x_min, f_min, _ = solve(
            wrapped_f,
            bounds.lowers,
            bounds.uppers,
            *self.direct_args,
            **self.direct_kwargs
        )

        return np.array(x_min), f_min
