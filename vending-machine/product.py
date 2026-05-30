class Product:
    def __init__(self, name: str, price: int) -> None:
        self.name = name
        self.price = price

    def get_price(self) -> int:
        return self.price

    def get_item(self) -> str:
        return self.name
