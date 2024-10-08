# Built-in dependencies
from typing import Dict

# External dependencies
import pandas as pd


class AmmortizationSchedule:

    def __init__(self, debt: float, rate: float, n_periods: int) -> None:
        """
        Args:
            n (int): Number of periods (total number of payments).
            debt (float): Present value or principal (loan amount).
            rate (float): Interest rate per period (e.g., monthly interest rate).
        """

        self.debt = debt
        self.rate = rate
        self.n_periods = n_periods
        self.payment = self._calculate_payment()

        self.schedule: pd.DataFrame = self._calculate_ammortization_schedule()

        return

    @staticmethod
    def _calculate_interest(debt: float, rate: float) -> float:
        return debt * rate

    @staticmethod
    def _calculate_principal(payment: float, interest: float) -> float:
        return payment - interest

    @staticmethod
    def _calculate_debt(debt: float, principal: float) -> float:
        return debt - principal

    @staticmethod
    def _calculate_equity(equity: float, principal: float) -> float:
        return equity + principal

    def _calculate_payment(self) -> float:
        """
        Computes the periodic payment that accounts for principal, interest, and compunding.
        """

        if self.rate == 0.0:

            # If zero interest rate, return equally divied payments of the outstanding debt
            return self.debt / self.n_periods

        else:

            # Scale periodic interest on outstanding debt by a discount rate that accounts for compounding
            return (self.debt * self.rate) / (1 - 1 / (1 + self.rate) ** self.n_periods)

    def _calculate_ammortization_schedule(self) -> pd.DataFrame:

        equity: float = 0.0
        debt: float = self.debt

        schedule: Dict[int, Dict[str, float]] = {}

        for t in range(self.n_periods):

            schedule[t] = {}

            schedule[t]["payment"] = self.payment
            schedule[t]["interest"] = self._calculate_interest(rate=self.rate, debt=debt)
            schedule[t]["principal"] = self._calculate_principal(payment=self.payment, interest=schedule[t]["interest"])

            debt = self._calculate_debt(debt=debt, principal=schedule[t]["principal"])
            equity = self._calculate_equity(equity=equity, principal=schedule[t]["principal"])

            schedule[t]["debt"] = debt
            schedule[t]["equity"] = equity

        return pd.DataFrame(schedule).T

    def plot(self) -> None:

        self.schedule[["debt", "equity"]].plot(title="Debt vs. Equity Schedule")
        self.schedule[["interest", "principal", "payment"]].plot(title="Ammortization Schedule")

        return
