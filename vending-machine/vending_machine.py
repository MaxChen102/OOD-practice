from __future__ import annotations

from coin import Coin
from inventory import Inventory
from product import Product
from state import IdleState, State


class VendingMachine:
    _instance: VendingMachine | None = None
    _initialized: bool = False

    def __new__(cls) -> VendingMachine:
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        if VendingMachine._initialized:
            return
        self.inventory = Inventory()
        self.balance = 0
        self.selected_item: Product | None = None
        self.state: State = IdleState(self)
        VendingMachine._initialized = True

    def insert_coin(self, coin: Coin) -> None:
        self.state.insert_coin(coin)

    def add_item(self, item: Product, quantity: int) -> None:
        self.inventory.add_item(item, quantity)

    def select_item(self, product: Product) -> None:
        self.state.select_product(product)

    def refund(self) -> int:
        return self.state.refund()

    def dispense(self) -> int:
        return self.state.dispense()

    def set_state(self, state: State) -> None:
        self.state = state
