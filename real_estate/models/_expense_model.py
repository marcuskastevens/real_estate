"""
TODO: Vectorize growth of random variables over time.
TODO: This can be done through a randomly simulated 'growth_adjustment_factor' which can be scaled by vectorized random variable simulations.
TODO: Build expense model configs and simply pass expenses as kwargs. This simplifies the code a lot. We can then just loop through kwargs.
"""

# Built-in dependencies
from typing import Dict, Optional, Tuple, Union

# External dependencies
import numpy as np

# Local dependencies
from real_estate.models.random_variables import RandomVariable
from real_estate.utils.model_utils import simulate_random_variable


class ExpenseModel:
    """
    Supports both constants and random variables.
    """

    def __init__(self, **expenses: Dict[str, Union[float, int, RandomVariable]]) -> None:

        self.expenses = expenses

        self._validate_expenses()

        return

    def _validate_expenses(self) -> None:

        for expense_key, expense in self.expenses.items():

            assert isinstance(expense, (float, int, RandomVariable)) or expense is None, (expense_key, expense)

        return

    def __call__(self, shape: Optional[Tuple[int, int]] = None) -> Union[float, np.ndarray]:

        total_expenses = np.zeros(shape=shape) if shape else 0.0

        for expense in self.expenses.values():
            total_expenses += simulate_random_variable(random_variable=expense, shape=shape)

        return total_expenses
