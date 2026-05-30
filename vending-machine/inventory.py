from product import Product


class Inventory:
    def __init__(self) -> None:
        self._stock: dict[str, tuple[Product, int]] = {}

    def add_item(self, item: Product, quantity: int) -> None:
        if quantity < 0:
            raise ValueError("quantity must be non-negative")
        if item.name in self._stock:
            product, current = self._stock[item.name]
            self._stock[item.name] = (product, current + quantity)
        else:
            self._stock[item.name] = (item, quantity)

    def get_item(self, name: str) -> Product:
        if name not in self._stock:
            raise KeyError(f"Unknown product: {name}")
        return self._stock[name][0]

    def is_avaiable(self, name: str) -> bool:
        if name not in self._stock:
            return False
        return self._stock[name][1] > 0

    def reduce_stock(self, name: str) -> None:
        if not self.is_avaiable(name):
            raise ValueError(f"{name} is out of stock")
        product, quantity = self._stock[name]
        self._stock[name] = (product, quantity - 1)
