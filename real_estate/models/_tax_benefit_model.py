# Built-in dependencies
from typing import Union

# External dependencies
import numpy as np


class TaxBenefitModel:

    def __init__(self, n: int, property_value: Union[float, int]) -> None:

        self.n = n
        self.property_value = property_value

        self._validate_kwargs()

        return

    def _validate_kwargs(self) -> None:

        assert isinstance(self.n, int), self.n
        assert isinstance(self.property_value, (float, int)), self.property_value

        return

    def __call__(self, interest_expense: Union[float, int, np.ndarray]) -> Union[float, np.ndarray]:
        """
        TODO: determine the true calculation - this is a rough proxy for now.
        """

        uncertainty_discount_factor = 1.0  # 0.5
        depreciation_deduction = self.property_value / self.n
        interest_deduction = interest_expense * 0.3
        property_tax_deduction = min(10_000.0, self.property_value * 0.02 / 12)

        return interest_deduction + depreciation_deduction * uncertainty_discount_factor + property_tax_deduction
