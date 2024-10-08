class TaxBenefitModel:

    def __call__(self, n: int, interest_expense: float, property_value: float) -> float:
        """
        TODO: determine the true calculation - this is a rough proxy for now.
        """

        uncertainty_discount_factor = 0.5
        depreciation_deduction = property_value / n
        interest_deduction = interest_expense * 0.3
        property_tax_deduction = min(10_000.0, property_value * 0.02 / 12)

        return interest_deduction + depreciation_deduction * uncertainty_discount_factor + property_tax_deduction
