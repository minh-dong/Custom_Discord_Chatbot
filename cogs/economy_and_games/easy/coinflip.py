#
#
#


import discord
from discord.ext import commands
from economy.models.account import Account
import peewee
import random


class CoinFlip(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.hybrid_command(name="coinflip",
                                 brief="Coin flip with heads or tails!",
                                 description="Coin flip with heads or tails to win/lose money!")
    async def coinflip(self, ctx, choice: str, amount: int):
        account = Account.fetch(ctx.message)

        if amount > account.amount:
            await ctx.send("You don't have enough credits.")
            return

        heads = random.randint(0,1)

        won = False
        if heads and choice.lower().startswith("h"):
            won = True
            account.amount += amount
        elif not heads and choice.lower().startswith("t"):
            won = True
            account.amount += amount
        else:
            account.amount -= amount

        account.save()

        message: str = "You lost!"
        if won:
            message = "You won!"

        await ctx.send(message)


# To add the bot to the cogs list
async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(CoinFlip(bot))
