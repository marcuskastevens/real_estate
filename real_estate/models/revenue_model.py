class RevenueModel:

    def __call__(self, rent: float, occupancy_rate: float) -> float:
        """
        Args:
            rent (float): Expected monthly rent.
            occupancy_rate (float): Expected occupancy rate as a fraction.
        """
        return rent * occupancy_rate
