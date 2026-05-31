class CashDispenser:
    def __init__(self, cash_on_hand: int = 10_000) -> None:
        self._cash_on_hand = cash_on_hand

    def can_dispense(self, amount: int) -> bool:
        return amount > 0 and self._cash_on_hand >= amount

    def dispense(self, amount: int) -> None:
        if amount <= 0:
            raise ValueError("dispense amount must be positive")
        if not self.can_dispense(amount):
            raise ValueError("ATM has insufficient cash to dispense")
        self._cash_on_hand -= amount

    def accept_cash(self, amount: int) -> None:
        if amount <= 0:
            raise ValueError("deposit amount must be positive")
        self._cash_on_hand += amount
