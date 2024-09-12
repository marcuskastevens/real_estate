class RevenueModel:

    def __call__(self, rent: float, occupancy_rate: float) -> float:
        """
        TODO: create time varying paths of rents, occupancy_rate, etc.

        Args:
            rent (float): Expected monthly rent.
            occupancy_rate (float): Expected occupancy rate as a fraction.
        """
        return rent * occupancy_rate
