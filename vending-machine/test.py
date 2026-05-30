import unittest

from coin import Coin
from product import Product
from state import DispensingState
from vending_machine import VendingMachine


def reset_vending_machine() -> VendingMachine:
    VendingMachine._instance = None
    VendingMachine._initialized = False
    return VendingMachine()


def stock_quantity(vm: VendingMachine, name: str) -> int:
    return vm.inventory._stock[name][1]


class TestVendingMachine(unittest.TestCase):
    def setUp(self) -> None:
        self.vm = reset_vending_machine()

    def test_add_item_sets_name_and_quantity(self) -> None:
        product = Product("Cola", 1.50)
        self.vm.add_item(product, 5)

        stored = self.vm.inventory.get_item("Cola")
        self.assertEqual(stored.get_item(), "Cola")
        self.assertEqual(stored.name, "Cola")
        self.assertEqual(stock_quantity(self.vm, "Cola"), 5)

    def test_buy_item_with_overpayment_returns_change(self) -> None:
        product = Product("Chips", 2.00)
        self.vm.add_item(product, 1)
        self.vm.select_item(product)
        self.vm.insert_coin(Coin.TOONIE)
        self.vm.insert_coin(Coin.QUARTER)
        self.vm.insert_coin(Coin.QUARTER)

        change = self.vm.dispense()

        self.assertAlmostEqual(change, 0.50)
        self.assertEqual(self.vm.balance, 0)
        self.assertFalse(self.vm.inventory.is_avaiable("Chips"))

    def test_add_item_with_negative_quantity_raises(self) -> None:
        product = Product("Candy", 1.00)
        with self.assertRaises(ValueError):
            self.vm.add_item(product, -1)

    def test_dispense_with_insufficient_balance_raises_message(self) -> None:
        product = Product("Water", 2.00)
        self.vm.add_item(product, 1)
        self.vm.select_item(product)
        self.vm.insert_coin(Coin.LOONIE)

        with self.assertRaises(ValueError) as ctx:
            self.vm.dispense()

        self.assertEqual(str(ctx.exception), "Insufficient funds")

    def test_refund_while_dispensing_raises(self) -> None:
        product = Product("Juice", 2.00)
        self.vm.add_item(product, 1)
        self.vm.select_item(product)
        self.vm.insert_coin(Coin.TOONIE)
        self.vm.set_state(DispensingState(self.vm))

        with self.assertRaises(ValueError) as ctx:
            self.vm.refund()

        self.assertEqual(str(ctx.exception), "Cannot refund while dispensing")


if __name__ == "__main__":
    unittest.main()
