## Requirements
1. The ATM system should support basic operations such as balance inquiry, cash withdrawal, and cash deposit.
2. Users should be able to authenticate themselves using a card and a PIN (Personal Identification Number).
3. The system should interact with a bank's backend system to validate user accounts and perform transactions.
4. The ATM should have a cash dispenser to dispense cash to users.
5. The ATM should have a user-friendly interface for users to interact with

## Classes and Methods

### ATM
- attributes:
- current state
- current card
- bank service

- methods:
- select_operation
- insert_card
- enter_pin
- deposit
- change_state
- check_balance
- withdraw

### BankService
- attributes:
- map cards to account
- map card number to Cards
- map account number to Accounts

- methods:
- link card to account
- authenticate card and account
- getBalance
- withdraw
- deposit

### Card
- attributes:
- card number (str)
- pin

### Account
- attributes:
- maps card numbers to Cards
- account number
- balance

- methods:
- withdraw
- deposit

### State
- methods:
- insert_card
- enter_pin
- select_operation
- eject_card

### IdleState(State)

### HasCardState(State)

### AutheticatedState(State)
