from __future__ import annotations

from abc import ABC, abstractmethod
from enum import Enum
from typing import TYPE_CHECKING

from card import Card

if TYPE_CHECKING:
    from atm import ATM


class Operation(Enum):
    CHECK_BALANCE = "check_balance"
    WITHDRAW = "withdraw"
    DEPOSIT = "deposit"
    EJECT_CARD = "eject_card"


class State(ABC):
    def __init__(self, atm: ATM) -> None:
        self.atm = atm

    @abstractmethod
    def insert_card(self, card: Card) -> None:
        ...

    @abstractmethod
    def enter_pin(self, pin: str) -> None:
        ...

    @abstractmethod
    def select_operation(self, operation: Operation) -> None:
        ...

    @abstractmethod
    def eject_card(self) -> None:
        ...


class IdleState(State):
    def insert_card(self, card: Card) -> None:
        if not self.atm.bank_service.is_registered(card):
            raise ValueError(f"unknown card: {card.card_number}")
        self.atm.current_card = card
        self.atm.change_state(HasCardState(self.atm))

    def enter_pin(self, pin: str) -> None:
        raise ValueError("insert a card before entering PIN")

    def select_operation(self, operation: Operation) -> None:
        raise ValueError("insert a card before selecting an operation")

    def eject_card(self) -> None:
        raise ValueError("no card to eject")


class HasCardState(State):
    def insert_card(self, card: Card) -> None:
        raise ValueError("eject the current card before inserting another")

    def enter_pin(self, pin: str) -> None:
        card = self.atm.current_card
        if card is None:
            raise ValueError("no card inserted")
        if not self.atm.bank_service.authenticate(card, pin):
            raise ValueError("invalid PIN")
        self.atm.change_state(AutheticatedState(self.atm))

    def select_operation(self, operation: Operation) -> None:
        raise ValueError("enter PIN before selecting an operation")

    def eject_card(self) -> None:
        self.atm.current_card = None
        self.atm.selected_operation = None
        self.atm.change_state(IdleState(self.atm))


class AutheticatedState(State):
    def insert_card(self, card: Card) -> None:
        raise ValueError("eject the current card before inserting another")

    def enter_pin(self, pin: str) -> None:
        raise ValueError("already authenticated")

    def select_operation(self, operation: Operation) -> None:
        if operation is Operation.EJECT_CARD:
            self.eject_card()
            return
        self.atm.selected_operation = operation

    def eject_card(self) -> None:
        self.atm.current_card = None
        self.atm.selected_operation = None
        self.atm.change_state(IdleState(self.atm))
