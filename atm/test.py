import unittest

from account import Account
from atm import ATM
from bank_service import BankService
from card import Card
from cash_dispenser import CashDispenser
from state import IdleState


def new_atm(initial_balance: int = 0) -> tuple[ATM, Card, Account]:
    bank = BankService()
    card = Card("4111-1111-1111-1111", "1234")
    account = Account("ACC-001", initial_balance)
    bank.link_card_to_account(card, account)
    atm = ATM(bank, CashDispenser(10_000))
    return atm, card, account


def authenticate(atm: ATM, card: Card, pin: str = "1234") -> None:
    atm.insert_card(card)
    atm.enter_pin(pin)


class TestATM(unittest.TestCase):
    def test_deposit_and_withdraw_updates_balance(self) -> None:
        atm, card, _ = new_atm()

        authenticate(atm, card)
        atm.deposit(200)
        atm.withdraw(100)

        self.assertEqual(atm.check_balance(), 100)

    def test_insert_and_eject_returns_same_card(self) -> None:
        atm, card, _ = new_atm()

        atm.insert_card(card)
        self.assertIs(atm.current_card, card)

        atm.eject_card()
        self.assertIsNone(atm.current_card)
        self.assertIsInstance(atm.state, IdleState)

        atm.insert_card(card)
        self.assertIs(atm.current_card, card)

    def test_deposit_negative_amount_raises(self) -> None:
        atm, card, _ = new_atm()
        authenticate(atm, card)

        with self.assertRaises(ValueError) as ctx:
            atm.deposit(-50)

        self.assertEqual(str(ctx.exception), "deposit amount must be positive")

    def test_deposit_zero_raises(self) -> None:
        atm, card, _ = new_atm()
        authenticate(atm, card)

        with self.assertRaises(ValueError) as ctx:
            atm.deposit(0)

        self.assertEqual(str(ctx.exception), "deposit amount must be positive")

    def test_withdraw_zero_raises(self) -> None:
        atm, card, _ = new_atm(initial_balance=500)
        authenticate(atm, card)

        with self.assertRaises(ValueError):
            atm.withdraw(0)

    def test_withdraw_negative_amount_raises(self) -> None:
        atm, card, _ = new_atm(initial_balance=500)
        authenticate(atm, card)

        with self.assertRaises(ValueError):
            atm.withdraw(-100)

    def test_withdraw_more_than_balance_raises(self) -> None:
        atm, card, account = new_atm(initial_balance=100)
        authenticate(atm, card)

        with self.assertRaises(ValueError) as ctx:
            atm.withdraw(200)

        self.assertEqual(str(ctx.exception), "insufficient account balance")
        self.assertEqual(account.balance, 100)


if __name__ == "__main__":
    unittest.main()
