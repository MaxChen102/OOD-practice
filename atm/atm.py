from __future__ import annotations

from bank_service import BankService
from card import Card
from cash_dispenser import CashDispenser
from state import AutheticatedState, HasCardState, IdleState, Operation, State


class ATM:
    def __init__(
        self,
        bank_service: BankService | None = None,
        cash_dispenser: CashDispenser | None = None,
    ) -> None:
        self.bank_service = bank_service or BankService()
        self.cash_dispenser = cash_dispenser or CashDispenser()
        self.current_card: Card | None = None
        self.selected_operation: Operation | None = None
        self.state: State = IdleState(self)

    def change_state(self, state: State) -> None:
        self.state = state

    def insert_card(self, card: Card) -> None:
        self.state.insert_card(card)

    def enter_pin(self, pin: str) -> None:
        self.state.enter_pin(pin)

    def select_operation(self, operation: Operation) -> None:
        self.state.select_operation(operation)

    def eject_card(self) -> None:
        self.state.eject_card()

    def check_balance(self) -> int:
        self._require_authenticated()
        card = self._require_card()
        return self.bank_service.get_balance(card)

    def withdraw(self, amount: int) -> None:
        self._require_authenticated()
        card = self._require_card()
        if not self.cash_dispenser.can_dispense(amount):
            raise ValueError("ATM has insufficient cash to dispense")
        self.bank_service.withdraw(card, amount)
        self.cash_dispenser.dispense(amount)

    def deposit(self, amount: int) -> None:
        self._require_authenticated()
        card = self._require_card()
        self.cash_dispenser.accept_cash(amount)
        self.bank_service.deposit(card, amount)

    def _require_authenticated(self) -> None:
        if not isinstance(self.state, AutheticatedState):
            raise ValueError("authenticate before performing this operation")

    def _require_card(self) -> Card:
        if self.current_card is None:
            raise ValueError("no card inserted")
        return self.current_card
