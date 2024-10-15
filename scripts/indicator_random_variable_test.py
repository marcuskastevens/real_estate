# Local dependencies
from real_estate.utils.model_utils import simulate_random_variable 
from real_estate.models.random_variables import IndicatorRandomVariable


def main() -> None:
    
    random_variable: IndicatorRandomVariable = IndicatorRandomVariable(probability=0.99)

    print(simulate_random_variable(random_variable=random_variable))

    return

if __name__ == "__main__":
    main()
