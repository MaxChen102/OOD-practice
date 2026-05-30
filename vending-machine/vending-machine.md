## Requirements
1. The vending machine should support multiple products with different prices and quantities.
2. The machine should accept coins and notes of different denominations.
3. The machine should dispense the selected product and return change if necessary.
4. The machine should keep track of the available products and their quantities.
5. The machine should provide an interface for restocking products and collecting money.
6. The machine should handle exceptional scenarios, such as insufficient funds or out-of-stock products.

## Classes and Methods

### VendingMachine
- singleton (only 1 vending machine)
- has inventory, state, balance, selected item
- insert_coin()
- add_item()
- select_item()
- refund()
- dispense()
- set_state()

### Inventory
- has products
- keeps track of quantity of each product
- add_item(self, item: Item, quantity: int) -> None
- get_item(self, name: str) -> Item
- is_avaiable(self, name: str) -> bool
- reduce_stock(self, name: str) -> None

### Product
- price: int
- name: str
- get_price(self) -> int
- get_item(self) -> str

### IdleState
- insert_coin(self, coin: Coin), user must select item first before inserting coins
- select_product(self, product: Product), change state to ItemSelectedState
- dispense(self)
- refund(self)

### ItemSelectedState
- insert_coin(self, coin: Coin), if balance is enough, change state to HasEnoughMoneyState
- select_product(self, product: Product)
- dispense(self)
- refund(self), refund and change state back to Idle

### HasEnoughMoneyState
- insert_coin(self, coin: Coin), extra coins so it will be refunded after
- select_product(self, product: Product), don't let user change items
- dispense(self), set to DispenseState and return change
- refund(self), refund and change state back to Idle

### DispensingState
- insert_coin(self, coin: Coin)
- select_product(self, product: Product)
- dispense(self)
- refund(self)

### Coin
- Toonies ($2), Loonies ($1), Quarters ($0.25), Dimes ($0.10), Nickels ($0.05)
- get_value(self) -> int


