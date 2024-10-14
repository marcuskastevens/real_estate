# Built-in dependencies
from typing import Optional, Tuple, Union

# External dependencies
import numpy as np

# Local dependencies
from real_estate.models.random_variables import RandomVariable
from real_estate.utils.model_utils import simulate_random_variable


class RevenueModel:

    def __init__(self, rent: Union[float, int], occupancy_rate: Union[float, int, RandomVariable]) -> None:
        """
        Args:
            rent (float): Expected monthly rent.
            occupancy_rate (Optional[Union[float, RandomVariable]]): Expected occupancy rate as a fraction.
        """

        self.rent = rent
        self.occupancy_rate = occupancy_rate

        self._validate_kwargs()

        return

    def _validate_kwargs(self) -> None:

        assert isinstance(self.rent, (float, int))
        assert isinstance(self.occupancy_rate, (float, int, RandomVariable))

        return

    def __call__(self, shape: Optional[Tuple[int, int]] = None) -> Union[float, np.ndarray]:
        return self.rent * simulate_random_variable(random_variable=self.occupancy_rate, shape=shape)
