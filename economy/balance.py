
from economy.models.account import Account


def updateAccountBalance(account, winner: bool, amount: int):
    # the final amount to be used
    final_amount: int = amount

    # Make sure the account amount is never less than 0. If it is, just deduct the remaining points
    if account.amount < amount:
        final_amount = account.amount

    # Did the user win?
    if winner:
        account.amount += final_amount
    else:
        account.amount -= final_amount

    account.save()
