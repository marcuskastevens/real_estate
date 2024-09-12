# Built-in dependencies
from typing import Optional, Union, Tuple

# External dependencies
import numpy as np
import pandas as pd

# Local dependencies
from .expense_model import ExpenseModel
from .revenue_model import RevenueModel
from .random_variables import RandomVariable
from .tax_benefit_model import TaxBenefitModel
from .ammortization_model import AmmortizationSchedule


class MonteCarloSimulator:
    """
    TODO: account for growth rates of random variables.
    TODO: account for cap rate.
    TODO: account for NOI.
    TODO: account for a valuation model = NOI / cap rate.
    TODO: account for levered and unlevered IRR.
    TODO: account for my cash flow / return on 1) equity 2) my true return which really captures what equity + cash flow I get for my initial investment + periodic cash flow injections.
    """

    def __init__(
        self,
        n: int,
        debt: float,
        rate: float,
        rent: float,
        equity: float,
        n_simulations: int,
        expense_model: ExpenseModel,
        revenue_model: RevenueModel,
        tax_benefit_model: TaxBenefitModel,
        occupancy_rate: RandomVariable,
        utility_expense: RandomVariable,
        insurance_expense: RandomVariable,
        maintenance_expense: RandomVariable,
        property_tax_expense: RandomVariable,
        miscellaneous_expense: RandomVariable,
    ) -> None:

        self.n = n
        self.debt = debt
        self.rate = rate
        self.rent = rent
        self.equity = equity
        self.n_simulations = n_simulations
        self.expense_model = expense_model
        self.revenue_model = revenue_model
        self.tax_benefit_model = tax_benefit_model
        self.occupancy_rate = occupancy_rate
        self.utility_expense = utility_expense
        self.insurance_expense = insurance_expense
        self.maintenance_expense = maintenance_expense
        self.property_tax_expense = property_tax_expense
        self.miscellaneous_expense = miscellaneous_expense

        self.shape: Tuple[int, int] = (self.n, self.n_simulations)
        self.property_value: float = self.debt + self.equity
        self.ammortization_schedule = AmmortizationSchedule(
            n=self.n, debt=self.debt, rate=self.rate
        )

        self.revenue_simulation: Optional[Union[np.ndarray, pd.DataFrame]] = None
        self.expense_simulation: Optional[Union[np.ndarray, pd.DataFrame]] = None
        self.cash_flow_simulation: Optional[Union[np.ndarray, pd.DataFrame]] = None
        self.tax_benefit_simulation: Optional[Union[np.ndarray, pd.DataFrame]] = None

        return

    def _simulate(self) -> Tuple[float, float, float]:
        """
        Capture

        Returns:
            Tuple[float, float, float]: _description_
        """

        revenue: Union[float, np.ndarray] = self.revenue_model(
            rent=self.rent,
            occupancy_rate=self.occupancy_rate.simulate(shape=self.shape),
        )

        tax_benefit: Union[float, np.ndarray] = (
            np.zeros(shape=self.shape) + 100.0
        )  # TODO: implement this in a vectorized manner - self.tax_benefit_model(n=self.n, interest_expense=interest_expense, property_value=self.property_value)

        interest_expense: np.ndarray = np.reshape(
            np.array(self.ammortization_schedule.schedule["interest"]), newshape=(-1, 1)
        )

        expenses: Union[float, np.ndarray] = self.expense_model(
            interest_expense=interest_expense,
            utility_expense=self.utility_expense.simulate(shape=self.shape),
            insurance_expense=self.insurance_expense.simulate(shape=self.shape),
            maintenance_expense=self.maintenance_expense.simulate(shape=self.shape),
            property_tax_expense=self.property_tax_expense.simulate(shape=self.shape),
            miscellaneous_expense=self.miscellaneous_expense.simulate(shape=self.shape),
        )

        cash_flow: np.ndarray = revenue + tax_benefit - expenses

        return revenue, tax_benefit, expenses, cash_flow

    def run(self) -> pd.DataFrame:

        (
            self.revenue_simulation,
            self.tax_benefit_simulation,
            self.expense_simulation,
            self.cash_flow_simulation,
        ) = self._simulate()

        self.revenue_simulation = pd.DataFrame(self.revenue_simulation)
        self.expense_simulation = pd.DataFrame(self.expense_simulation)
        self.cash_flow_simulation = pd.DataFrame(self.cash_flow_simulation)
        self.tax_benefit_simulation = pd.DataFrame(self.tax_benefit_simulation)

        return

    def analyze(self) -> None:
        """
        Analyze the results of the Monte Carlo simulation, such as expected profit/loss.
        """

        if self.cash_flow_simulation is None:
            self.run()

        cumulative_cash_flows = np.sum(self.cash_flow_simulation, axis=0)

        print(f"Terminal Cash Flow Mean: {cumulative_cash_flows.mean()}")
        print(f"Terminal Cash Flow Min: {cumulative_cash_flows.min()}")
        print(f"Terminal Cash Flow Max: {cumulative_cash_flows.max()}")
        print(f"Periodic Cash Flow Mean: {np.mean(self.cash_flow_simulation)}")
        print(
            f"Periodic Cash Flow Standard Deviation: {np.std(self.cash_flow_simulation.to_numpy().flatten(), ddof=1)}"
        )
        print(
            f"Cash Flow Mean Sharpe Ratio: {np.mean(self.cash_flow_simulation) / np.std(self.cash_flow_simulation.to_numpy().flatten(), ddof=1)}"
        )

        self.cash_flow_simulation.plot(title="Periodic Cash Flows", legend=False)
        self.cash_flow_simulation.plot(
            kind="hist", title="Periodic Cash Flows", legend=False
        )
        self.cash_flow_simulation.cumsum().plot(
            title="Cumulative Cash Flows", legend=False
        )

        self.revenue_simulation.plot(
            kind="hist", title="Periodic Revenue", legend=False
        )
        self.expense_simulation.plot(
            kind="hist", title="Periodic Expenses", legend=False
        )
        self.expense_simulation.plot(title="Periodic Expenses", legend=False)
        self.tax_benefit_simulation.plot(title="Periodic Tax Benefit", legend=False)

        return
