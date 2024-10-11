"""
TODO: Vectorize growth of random variables throughout time.
TODO: This can be done through a randomly simulated 'growth_adjustment_factor' which can be scaled by vectorized random variable simulations.
TODO: Build expense model configs and simply pass expenses as kwargs. This simplifies the code a lot. We can then just loop through kwargs.
"""

# Built-in dependencies
from typing import Optional, Tuple, Union

# External dependencies
import numpy as np

# Local dependencies
from .random_variables import RandomVariable


def simulate_random_variable(
    random_variable: Optional[Union[float, RandomVariable]],
    shape: Optional[Tuple[int, int]],
) -> Union[float, np.ndarray]:

    assert isinstance(shape, Tuple) or shape is None, shape
    assert isinstance(random_variable, (float, RandomVariable)) or random_variable is None, random_variable

    if isinstance(random_variable, RandomVariable):
        simulated_random_variable = random_variable.simulate(shape=shape)
    elif isinstance(random_variable, float):
        simulated_random_variable = np.full(shape=shape, fill_value=random_variable) if shape else random_variable
    else:
        simulated_random_variable = np.zeros(shape=shape) if shape else 0.0

    return simulated_random_variable


class ExpenseModel:
    """
    Supports both constants and random variables.
    """

    def __init__(
        self,
        hoa_expense: Optional[Union[float, RandomVariable]] = None,
        loan_expense: Optional[Union[float, RandomVariable]] = None,
        legal_expense: Optional[Union[float, RandomVariable]] = None,
        permit_expense: Optional[Union[float, RandomVariable]] = None,
        leasing_expense: Optional[Union[float, RandomVariable]] = None,
        utility_expense: Optional[Union[float, RandomVariable]] = None,
        security_expense: Optional[Union[float, RandomVariable]] = None,
        software_expense: Optional[Union[float, RandomVariable]] = None,
        insurance_expense: Optional[Union[float, RandomVariable]] = None,
        appraisal_expense: Optional[Union[float, RandomVariable]] = None,
        marketing_expense: Optional[Union[float, RandomVariable]] = None,
        furnishing_expense: Optional[Union[float, RandomVariable]] = None,
        inspection_expense: Optional[Union[float, RandomVariable]] = None,
        accounting_expense: Optional[Union[float, RandomVariable]] = None,
        landscaping_expense: Optional[Union[float, RandomVariable]] = None,
        maintenance_expense: Optional[Union[float, RandomVariable]] = None,
        refinancing_expense: Optional[Union[float, RandomVariable]] = None,
        advertising_expense: Optional[Union[float, RandomVariable]] = None,
        property_tax_expense: Optional[Union[float, RandomVariable]] = None,
        pest_control_expense: Optional[Union[float, RandomVariable]] = None,
        miscellaneous_expense: Optional[Union[float, RandomVariable]] = None,
        tenant_incentive_expense: Optional[Union[float, RandomVariable]] = None,
        property_management_expense: Optional[Union[float, RandomVariable]] = None,
        capital_expenditure_expense: Optional[Union[float, RandomVariable]] = None,
        insurance_deductible_expense: Optional[Union[float, RandomVariable]] = None,
        regulatory_compliance_expense: Optional[Union[float, RandomVariable]] = None,
        professional_development_expense: Optional[Union[float, RandomVariable]] = None,
    ) -> None:

        self.hoa_expense = hoa_expense
        self.loan_expense = loan_expense
        self.legal_expense = legal_expense
        self.permit_expense = permit_expense
        self.leasing_expense = leasing_expense
        self.utility_expense = utility_expense
        self.security_expense = security_expense
        self.software_expense = software_expense
        self.insurance_expense = insurance_expense
        self.appraisal_expense = appraisal_expense
        self.marketing_expense = marketing_expense
        self.furnishing_expense = furnishing_expense
        self.inspection_expense = inspection_expense
        self.accounting_expense = accounting_expense
        self.landscaping_expense = landscaping_expense
        self.maintenance_expense = maintenance_expense
        self.refinancing_expense = refinancing_expense
        self.advertising_expense = advertising_expense
        self.property_tax_expense = property_tax_expense
        self.pest_control_expense = pest_control_expense
        self.miscellaneous_expense = miscellaneous_expense
        self.tenant_incentive_expense = tenant_incentive_expense
        self.property_management_expense = property_management_expense
        self.capital_expenditure_expense = capital_expenditure_expense
        self.insurance_deductible_expense = insurance_deductible_expense
        self.regulatory_compliance_expense = regulatory_compliance_expense
        self.professional_development_expense = professional_development_expense

        return

    def __call__(self, shape: Optional[Tuple[int, int]] = None) -> float:
        """
        Returns the total of all real estate-related expenses by summing them into categories.
        """

        # Operating expenses
        operating_expenses = (
            simulate_random_variable(random_variable=self.hoa_expense, shape=shape)
            + simulate_random_variable(random_variable=self.loan_expense, shape=shape)
            + simulate_random_variable(random_variable=self.legal_expense, shape=shape)
            + simulate_random_variable(random_variable=self.permit_expense, shape=shape)
            + simulate_random_variable(random_variable=self.leasing_expense, shape=shape)
            + simulate_random_variable(random_variable=self.utility_expense, shape=shape)
            + simulate_random_variable(random_variable=self.security_expense, shape=shape)
            + simulate_random_variable(random_variable=self.software_expense, shape=shape)
            + simulate_random_variable(random_variable=self.insurance_expense, shape=shape)
            + simulate_random_variable(random_variable=self.marketing_expense, shape=shape)
            + simulate_random_variable(random_variable=self.furnishing_expense, shape=shape)
            + simulate_random_variable(random_variable=self.accounting_expense, shape=shape)
            + simulate_random_variable(random_variable=self.inspection_expense, shape=shape)
            + simulate_random_variable(random_variable=self.landscaping_expense, shape=shape)
            + simulate_random_variable(random_variable=self.maintenance_expense, shape=shape)
            + simulate_random_variable(random_variable=self.advertising_expense, shape=shape)
            + simulate_random_variable(random_variable=self.property_tax_expense, shape=shape)
            + simulate_random_variable(random_variable=self.pest_control_expense, shape=shape)
            + simulate_random_variable(random_variable=self.miscellaneous_expense, shape=shape)
            + simulate_random_variable(random_variable=self.tenant_incentive_expense, shape=shape)
            + simulate_random_variable(random_variable=self.property_management_expense, shape=shape)
            + simulate_random_variable(random_variable=self.professional_development_expense, shape=shape)
        )

        # Capital expenditures
        capital_expenditures = simulate_random_variable(
            random_variable=self.capital_expenditure_expense,
            shape=shape,
        )

        # Financing & transaction costs
        financing_and_transaction_expenses = (
            simulate_random_variable(random_variable=self.loan_expense, shape=shape)
            + simulate_random_variable(random_variable=self.appraisal_expense, shape=shape)
            + simulate_random_variable(random_variable=self.inspection_expense, shape=shape)
            + simulate_random_variable(random_variable=self.refinancing_expense, shape=shape)
        )

        # One-time or rare expenses
        one_time_expenses = (
            simulate_random_variable(random_variable=self.permit_expense, shape=shape)
            + simulate_random_variable(random_variable=self.furnishing_expense, shape=shape)
            + simulate_random_variable(random_variable=self.insurance_deductible_expense, shape=shape)
            + simulate_random_variable(random_variable=self.regulatory_compliance_expense, shape=shape)
        )

        # Total sum of all categorized expenses
        return operating_expenses + capital_expenditures + financing_and_transaction_expenses + one_time_expenses
