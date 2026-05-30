from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

from coin import Coin
from product import Product

if TYPE_CHECKING:
    from vending_machine import VendingMachine


class State(ABC):
    def __init__(self, machine: VendingMachine) -> None:
        self.machine = machine

    @abstractmethod
    def insert_coin(self, coin: Coin) -> None:
        ...

    @abstractmethod
    def select_product(self, product: Product) -> None:
        ...

    @abstractmethod
    def dispense(self) -> int:
        ...

    @abstractmethod
    def refund(self) -> int:
        ...


class IdleState(State):
    def insert_coin(self, coin: Coin) -> None:
        raise ValueError("Select an item before inserting coins")

    def select_product(self, product: Product) -> None:
        if not self.machine.inventory.is_avaiable(product.name):
            raise ValueError(f"{product.name} is out of stock")
        self.machine.selected_item = product
        self.machine.set_state(ItemSelectedState(self.machine))

    def dispense(self) -> int:
        raise ValueError("No item selected")

    def refund(self) -> int:
        return 0


class ItemSelectedState(State):
    def insert_coin(self, coin: Coin) -> None:
        self.machine.balance += coin.get_value()
        selected = self.machine.selected_item
        if selected is not None and self.machine.balance >= selected.get_price():
            self.machine.set_state(HasEnoughMoneyState(self.machine))

    def select_product(self, product: Product) -> None:
        if not self.machine.inventory.is_avaiable(product.name):
            raise ValueError(f"{product.name} is out of stock")
        self.machine.selected_item = product
        if self.machine.balance >= product.get_price():
            self.machine.set_state(HasEnoughMoneyState(self.machine))

    def dispense(self) -> int:
        selected = self.machine.selected_item
        if selected is None or self.machine.balance < selected.get_price():
            raise ValueError("Insufficient funds")
        self.machine.set_state(DispensingState(self.machine))
        return self.machine.state.dispense()

    def refund(self) -> int:
        amount = self.machine.balance
        self.machine.balance = 0
        self.machine.selected_item = None
        self.machine.set_state(IdleState(self.machine))
        return amount


class HasEnoughMoneyState(State):
    def insert_coin(self, coin: Coin) -> None:
        self.machine.balance += coin.get_value()

    def select_product(self, product: Product) -> None:
        raise ValueError("Cannot change item once sufficient funds are inserted")

    def dispense(self) -> int:
        self.machine.set_state(DispensingState(self.machine))
        return self.machine.state.dispense()

    def refund(self) -> int:
        amount = self.machine.balance
        self.machine.balance = 0
        self.machine.selected_item = None
        self.machine.set_state(IdleState(self.machine))
        return amount


class DispensingState(State):
    def insert_coin(self, coin: Coin) -> None:
        raise ValueError("Cannot insert coins while dispensing")

    def select_product(self, product: Product) -> None:
        raise ValueError("Cannot select product while dispensing")

    def dispense(self) -> int:
        selected = self.machine.selected_item
        if selected is None:
            raise ValueError("No item to dispense")
        self.machine.inventory.reduce_stock(selected.name)
        change = self.machine.balance - selected.get_price()
        self.machine.balance = 0
        self.machine.selected_item = None
        self.machine.set_state(IdleState(self.machine))
        return change

    def refund(self) -> int:
        raise ValueError("Cannot refund while dispensing")
