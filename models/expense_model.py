# Built-in dependencies
from typing import Union

# External dependencies
import numpy as np


class ExpenseModel:

    def __call__(
        self,
        hoa_expense: Union[float, np.ndarray] = 0.0,
        loan_expense: Union[float, np.ndarray] = 0.0,
        legal_expense: Union[float, np.ndarray] = 0.0,
        permit_expense: Union[float, np.ndarray] = 0.0,
        leasing_expense: Union[float, np.ndarray] = 0.0,
        utility_expense: Union[float, np.ndarray] = 0.0,
        security_expense: Union[float, np.ndarray] = 0.0,
        software_expense: Union[float, np.ndarray] = 0.0,
        insurance_expense: Union[float, np.ndarray] = 0.0,
        appraisal_expense: Union[float, np.ndarray] = 0.0,
        marketing_expense: Union[float, np.ndarray] = 0.0,
        furnishing_expense: Union[float, np.ndarray] = 0.0,
        inspection_expense: Union[float, np.ndarray] = 0.0,
        accounting_expense: Union[float, np.ndarray] = 0.0,
        landscaping_expense: Union[float, np.ndarray] = 0.0,
        maintenance_expense: Union[float, np.ndarray] = 0.0,
        refinancing_expense: Union[float, np.ndarray] = 0.0,
        advertising_expense: Union[float, np.ndarray] = 0.0,
        property_tax_expense: Union[float, np.ndarray] = 0.0,
        pest_control_expense: Union[float, np.ndarray] = 0.0,
        miscellaneous_expense: Union[float, np.ndarray] = 0.0,
        tenant_incentive_expense: Union[float, np.ndarray] = 0.0,
        property_management_expense: Union[float, np.ndarray] = 0.0,
        capital_expenditure_expense: Union[float, np.ndarray] = 0.0,
        insurance_deductible_expense: Union[float, np.ndarray] = 0.0,
        regulatory_compliance_expense: Union[float, np.ndarray] = 0.0,
        professional_development_expense: Union[float, np.ndarray] = 0.0,
    ) -> float:
        """
        Returns the total of all real estate-related expenses by summing them into categories.
        """

        # Operating Expenses
        operating_expenses = (
            hoa_expense
            + loan_expense
            + legal_expense
            + permit_expense
            + leasing_expense
            + utility_expense
            + security_expense
            + software_expense
            + insurance_expense
            + marketing_expense
            + furnishing_expense
            + accounting_expense
            + inspection_expense
            + landscaping_expense
            + maintenance_expense
            + advertising_expense
            + property_tax_expense
            + pest_control_expense
            + miscellaneous_expense
            + tenant_incentive_expense
            + property_management_expense
            + professional_development_expense
        )

        # Capital Expenditures
        capital_expenditures = capital_expenditure_expense

        # Financing & Transaction Costs
        financing_and_transaction_expenses = loan_expense + appraisal_expense + inspection_expense + refinancing_expense

        # One-Time or Rare Expenses
        one_time_expenses = (
            permit_expense + furnishing_expense + insurance_deductible_expense + regulatory_compliance_expense
        )

        # Total sum of all categorized expenses
        return operating_expenses + capital_expenditures + financing_and_transaction_expenses + one_time_expenses
