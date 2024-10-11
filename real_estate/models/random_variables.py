# Built-in dependencies
from abc import ABC, abstractmethod
from typing import Optional, Tuple

# External dependencies
import numpy as np


class RandomVariable(ABC):

    @abstractmethod
    def simulate(self, shape: Optional[Tuple[int, int]] = None) -> float:
        """
        Simulates a variable.
        """
        raise NotImplementedError


class NormalRandomVariable(RandomVariable):

    def __init__(self, mu: float, sigma: Optional[float] = None) -> None:

        self.mu = mu
        self.sigma = sigma

        return

    def simulate(self, shape: Optional[Tuple[int, int]] = None) -> float:
        """
        Simulates a normally distributed variable or a constant if no sigma (i.e., scale or standard deviation) is defined.
        """
        return np.random.normal(loc=self.mu, scale=self.sigma, size=shape) if self.sigma else self.mu


class LogNormalRandomVariable(RandomVariable):

    def __init__(self, mu: float, sigma: Optional[float] = None) -> None:

        self.mu = mu
        self.sigma = sigma

        return

    def simulate(self, shape: Optional[Tuple[int, int]] = None) -> float:
        """
        Simulates a log-normally distributed variable or a constant if no sigma (i.e., scale or standard deviation) is defined.
        """
        return (
            np.exp(np.random.normal(loc=self.mu - 0.5 * self.sigma**2, scale=self.sigma, size=shape)) - 1
            if self.sigma
            else self.mu
        )


class IndicatorRandomVariable(RandomVariable):

    def __init__(self, probability: float) -> None:

        self.probability = probability

        return

    def simulate(self, shape: Optional[Tuple[int, int]] = None) -> float:
        """
        Simulates an indicator random variables for a given probability.
        """
        return np.random.choice(a=[0, 1], p=[1 - self.probability, self.probability], size=shape)


class UniformRandomVariable(RandomVariable):

    def __init__(self, lower_bound: float, upper_bound: float) -> None:

        self.lower_bound = lower_bound
        self.upper_bound = upper_bound

        return

    def simulate(self, shape: Optional[Tuple[int, int]] = None) -> float:
        """
        Simulates a uniformly distributed variable.
        """
        return np.random.uniform(low=self.lower_bound, high=self.upper_bound, size=shape)


class BoundedNormalRandomVariable(RandomVariable):

    def __init__(self, mu: float, sigma: float, lower_bound: float, upper_bound: float) -> None:

        self.mu = mu
        self.sigma = sigma
        self.lower_bound = lower_bound
        self.upper_bound = upper_bound

        return

    def simulate(self, shape: Optional[Tuple[int, int]] = None) -> float:
        """
        Simulates a bounded normally distributed variable or a constant if no sigma (i.e., scale or standard deviation) is defined.
        """

        random_variable = np.random.normal(loc=self.mu, scale=self.sigma, size=shape)

        if shape:

            # While there are values outside of the bounds, regenerate only those values
            out_of_bounds = (random_variable <= self.lower_bound) | (random_variable >= self.upper_bound)

            while np.any(out_of_bounds):

                # Re-sample only the out-of-bound elements
                random_variable[out_of_bounds] = np.random.normal(
                    loc=self.mu,
                    scale=self.sigma,
                    size=np.sum(out_of_bounds),
                )

                # Update out-of-bound entries
                out_of_bounds = (random_variable <= self.lower_bound) | (random_variable >= self.upper_bound)

        else:

            # If the random variable is out-of-bounds, recursively re-sample
            if self.lower_bound <= random_variable <= self.upper_bound:
                random_variable = self.simulate(shape=shape)

        return random_variable
