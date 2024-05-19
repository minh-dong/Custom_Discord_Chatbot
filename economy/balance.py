
from economy.models.account import Account


def updateAccountBalance(account, winner: bool, amount: int):
    # Did the user win?
    if winner:
        account.amount += amount
    else:
        account.amount -= amount

    account.save()
