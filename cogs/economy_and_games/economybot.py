#
# Economy for Discord bot
#

import discord
from discord.ext import commands
from economy.models.account import Account


class EconomyBot(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.hybrid_command(name="balance",
                             brief="Get your balance",
                             description="Get your current balance")
    async def balance(self, ctx):
        account = Account.fetch(ctx.message)

        await ctx.send(f"Your balance is: {account.amount}")


# To add the bot to the cogs list
async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(EconomyBot(bot))
