"""
TODO: Vectorize growth of random variables throughout time.
TODO: This can be done through a randomly simulated 'growth_adjustment_factor' which can be scaled by vectorized random variable simulations.
TODO: Build expense model configs and simply pass expenses as kwargs. This simplifies the code a lot. We can then just loop through kwargs.
"""

# Built-in dependencies
from typing import Dict, Optional, Tuple, Union

# External dependencies
import numpy as np

# Local dependencies
from real_estate.utils import simulate_random_variable
from real_estate.models.random_variables import RandomVariable


class ExpenseModel:
    """
    Supports both constants and random variables.
    """

    def __init__(self, **kwargs: Dict[str, Union[float, RandomVariable]]) -> None:

        self.kwargs = kwargs

        self._validate_kwargs()

        return

    def _validate_kwargs(self) -> None:

        for expense_key, expense_random_variable in self.kwargs.items():

            assert isinstance(expense_random_variable, (float, RandomVariable)) or expense_random_variable is None, (
                expense_key,
                expense_random_variable,
            )

        return

    def __call__(self, shape: Optional[Tuple[int, int]] = None) -> Union[float, np.ndarray]:

        total_expenses = np.zeros(shape=shape) if shape else 0.0

        for expense_random_variable in self.kwargs.values():
            total_expenses += simulate_random_variable(random_variable=expense_random_variable, shape=shape)

        return total_expenses
