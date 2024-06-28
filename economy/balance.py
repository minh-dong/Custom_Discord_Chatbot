#
# A set of functions (or in this case only one at the moment) that manipulates the balance
#

def updateAccountBalance(account, winner: bool, amount: int) -> None:
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

    # Save the account to the SQLite database
    account.save()
