
import peewee
from economy import get_economy_database


class Account(peewee.Model):
    user_id: str = peewee.CharField(max_length=255)
    guild_id: str = peewee.CharField(max_length=255)
    amount: int = peewee.IntegerField()

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
                                     amount=0)
        return account