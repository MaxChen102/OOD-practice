from __future__ import annotations

from card import Card


class Account:
    def __init__(self, account_number: str, balance: int = 0) -> None:
        self.account_number = account_number
        self.balance = balance
        self._cards: dict[str, Card] = {}

    def link_card(self, card: Card) -> None:
        self._cards[card.card_number] = card

    def withdraw(self, amount: int) -> None:
        if amount <= 0:
            raise ValueError("withdrawal amount must be positive")
        if self.balance < amount:
            raise ValueError("insufficient account balance")
        self.balance -= amount

    def deposit(self, amount: int) -> None:
        if amount <= 0:
            raise ValueError("deposit amount must be positive")
        self.balance += amount
