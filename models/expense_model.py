class ExpenseModel:

    def __call__(
        self,
        utility_expense: float,
        interest_expense: float,
        insurance_expense: float,
        maintenance_expense: float,
        property_tax_expense: float,
        miscellaneous_expense: float,
    ) -> float:

        return (
            utility_expense
            + interest_expense
            + insurance_expense
            + maintenance_expense
            + property_tax_expense
            + miscellaneous_expense
        )
