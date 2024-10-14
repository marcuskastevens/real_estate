# Built-in dependencies
from typing import Optional, Tuple, Union

# External dependencies
import numpy as np

# Local dependencies
from real_estate.models.random_variables import RandomVariable


def simulate_random_variable(
    random_variable: Optional[Union[float, int, RandomVariable]],
    shape: Optional[Tuple[int, int]],
) -> Union[float, int, np.ndarray]:

    assert isinstance(shape, Tuple) or shape is None, shape
    assert isinstance(random_variable, (float, int, RandomVariable)) or random_variable is None, random_variable

    if isinstance(random_variable, RandomVariable):
        simulated_random_variable = random_variable.simulate(shape=shape)
    elif isinstance(random_variable, (float, int)):
        simulated_random_variable = np.full(shape=shape, fill_value=random_variable) if shape else random_variable
    else:
        simulated_random_variable = np.zeros(shape=shape) if shape else 0.0

    return simulated_random_variable
