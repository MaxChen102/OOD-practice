from enum import Enum


class Coin(Enum):
    TOONIE = 2.00
    LOONIE = 1.00
    QUARTER = 0.25
    DIME = 0.10
    NICKEL = 0.05

    def get_value(self) -> int:
        return self.value
