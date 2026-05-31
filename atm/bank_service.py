from account import Account
from card import Card


class BankService:
    def __init__(self) -> None:
        self._card_to_account: dict[str, str] = {}
        self._cards: dict[str, Card] = {}
        self._accounts: dict[str, Account] = {}

    def link_card_to_account(self, card: Card, account: Account) -> None:
        self._cards[card.card_number] = card
        self._accounts[account.account_number] = account
        account.link_card(card)
        self._card_to_account[card.card_number] = account.account_number

    def is_registered(self, card: Card) -> bool:
        return self._cards.get(card.card_number) is card

    def authenticate(self, card: Card, pin: str) -> bool:
        registered = self._cards.get(card.card_number)
        if registered is None or registered is not card:
            return False
        return card.pin == pin

    def _account_for_card(self, card: Card) -> Account:
        account_number = self._card_to_account.get(card.card_number)
        if account_number is None:
            raise ValueError(f"card {card.card_number} is not linked to an account")
        return self._accounts[account_number]

    def get_balance(self, card: Card) -> int:
        return self._account_for_card(card).balance

    def withdraw(self, card: Card, amount: int) -> None:
        self._account_for_card(card).withdraw(amount)

    def deposit(self, card: Card, amount: int) -> None:
        self._account_for_card(card).deposit(amount)
