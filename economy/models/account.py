#
# account.py is a class file for getting the account information. the fetch will fetch the user's data so info can be
# manipulated like account's amount (for economy purposes), next claim for the next time the user can claim their
# points, etc.
#

import peewee
from economy import get_economy_database
from datetime import datetime, timedelta


class Account(peewee.Model):
    user_id: str = peewee.CharField(max_length=255)
    guild_id: str = peewee.CharField(max_length=255)
    amount: int = peewee.IntegerField()
    next_claim: datetime = peewee.DateTimeField(default=datetime.now)

    class Meta:
        database = get_economy_database()

    @staticmethod
    def fetch(message):
        try:
            account = Account.get(Account.user_id == message.author.id,
                                         Account.guild_id == message.guild.id)
        except peewee.DoesNotExist:
            account = Account.create(user_id=message.author.id,
                                     guild_id=message.guild.id,
                                     amount=0,
                                     next_claim=datetime.now() - timedelta(hours=24))
        return account
