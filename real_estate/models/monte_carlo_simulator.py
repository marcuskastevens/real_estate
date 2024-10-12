# Built-in dependencies
from typing import Optional, Union, Tuple

# External dependencies
import numpy as np
import pandas as pd

# Local dependencies
from real_estate.models.expense_model import ExpenseModel
from real_estate.models.revenue_model import RevenueModel
from real_estate.models.tax_benefit_model import TaxBenefitModel
from real_estate.models.ammortization_model import AmmortizationSchedule


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
        debt: float,
        rate: float,
        equity: float,
        n_periods: int,
        n_simulations: int,
        expense_model: ExpenseModel,
        revenue_model: RevenueModel,
        tax_benefit_model: TaxBenefitModel,
    ) -> None:

        self.debt = debt
        self.rate = rate
        self.equity = equity
        self.n_periods = n_periods
        self.n_simulations = n_simulations
        self.expense_model = expense_model
        self.revenue_model = revenue_model
        self.tax_benefit_model = tax_benefit_model

        self.total_value: float = self.debt + self.equity
        self.shape: Tuple[int, int] = (self.n_periods, self.n_simulations)
        self.ammortization_schedule = AmmortizationSchedule(
            n_periods=self.n_periods,
            debt=self.debt,
            rate=self.rate,
        )

        self.revenue_simulation: Optional[Union[np.ndarray, pd.DataFrame]] = None
        self.cash_flow_simulation: Optional[Union[np.ndarray, pd.DataFrame]] = None
        self.tax_benefit_simulation: Optional[Union[np.ndarray, pd.DataFrame]] = None
        self.operating_expense_simulation: Optional[Union[np.ndarray, pd.DataFrame]] = None

        return

    def _simulate(self) -> Tuple[float, float, float]:

        revenue: Union[float, np.ndarray] = self.revenue_model(
            rent=self.rent,
            occupancy_rate=self.occupancy_rate.simulate(shape=self.shape),
        )

        tax_benefit = self.tax_benefit_model(
            n_periods=self.n_periods, interest_expense=interest_expense, property_value=self.property_value
        )

        interest_expense: np.ndarray = np.reshape(
            np.array(self.ammortization_schedule.schedule["interest"]),
            newshape=(-1, 1),
        )

        principal_expense: np.ndarray = np.reshape(
            np.array(self.ammortization_schedule.schedule["principal"]),
            newshape=(-1, 1),
        )

        operating_expense: Union[float, np.ndarray] = self.expense_model()

        equity: np.ndarray = np.reshape(np.array(self.ammortization_schedule.schedule["equity"]), newshape=(-1, 1))

        cash_flow: np.ndarray = revenue + tax_benefit - operating_expense - interest_expense - principal_expense

        # Total return is a function of both cash flow and increase in equity (i.e., how much principal is paid)
        total_return: np.ndarray = cash_flow + principal_expense

        # TODO: denominator omits the equity that was earned from each period
        cash_return_on_equity: np.ndarray = cash_flow / (equity + self.equity - principal_expense)
        total_return_on_equity: np.array = total_return / (equity + self.equity - principal_expense)

        # TODO: not sure if this makes any sense
        cumulative_cash_return_on_initial_equity: np.ndarray = np.cumsum(cash_flow, axis=0) / self.equity
        cumulative_total_return_on_initial_equity: np.ndarray = np.cumsum(total_return, axis=0) / self.equity

        return (
            revenue,
            tax_benefit,
            operating_expense,
            cash_flow,
            cash_return_on_equity,
            total_return_on_equity,
            cumulative_cash_return_on_initial_equity,
            cumulative_total_return_on_initial_equity,
        )

    def run(self) -> pd.DataFrame:

        (
            self.revenue_simulation,
            self.tax_benefit_simulation,
            self.operating_expense_simulation,
            self.cash_flow_simulation,
            self.cash_return_on_equity,
            self.total_return_on_equity,
            self.cumulative_cash_return_on_initial_equity,
            self.cumulative_total_return_on_initial_equity,
        ) = self._simulate()

        self.revenue_simulation = pd.DataFrame(self.revenue_simulation)
        self.cash_flow_simulation = pd.DataFrame(self.cash_flow_simulation)
        self.cash_return_on_equity = pd.DataFrame(self.cash_return_on_equity)
        self.total_return_on_equity = pd.DataFrame(self.total_return_on_equity)
        self.tax_benefit_simulation = pd.DataFrame(self.tax_benefit_simulation)
        self.operating_expense_simulation = pd.DataFrame(self.operating_expense_simulation)
        self.cumulative_cash_return_on_initial_equity = pd.DataFrame(self.cumulative_cash_return_on_initial_equity)
        self.cumulative_total_return_on_initial_equity = pd.DataFrame(self.cumulative_total_return_on_initial_equity)

        self.cash_cagr: pd.Series = (1 + self.cumulative_cash_return_on_initial_equity.iloc[-1]) ** (
            1 / (self.n_periods / 30)
        ) - 1
        self.total_cagr: pd.Series = (1 + self.cumulative_total_return_on_initial_equity.iloc[-1]) ** (
            1 / (self.n_periods / 30)
        ) - 1

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
        self.cash_flow_simulation.plot(kind="hist", title="Periodic Cash Flows", legend=False)
        self.cash_flow_simulation.cumsum().plot(title="Cumulative Cash Flows", legend=False)

        self.revenue_simulation.plot(kind="hist", title="Periodic Revenue", legend=False)
        self.expense_simulation.plot(kind="hist", title="Periodic Expenses", legend=False)
        self.expense_simulation.plot(title="Periodic Expenses", legend=False)
        self.tax_benefit_simulation.plot(title="Periodic Tax Benefit", legend=False)

        return
