#
# Economy for Discord bot
#

import discord
from discord.ext import commands
from economy.models.account import Account
from datetime import datetime, timedelta


class EconomyBot(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.hybrid_command(name="balance",
                             brief="Get your balance",
                             description="Get your current balance",
                             aliases=["bal", "money"])
    async def balance(self, ctx):
        account = Account.fetch(ctx.message)

        await ctx.send(f"Your balance is: {account.amount}")

    # @todo - add this command and stuff
    @commands.hybrid_command(name="claim",
                             brief="Claim your free coins!",
                             description="Claim your free daily coins!",
                             aliases=["daily"])
    async def claim(self, ctx):
        account = Account.fetch(ctx.message)

        # Get the next_claim from the sql database
        past = account.next_claim
        now = datetime.now()
        future = datetime.now() + timedelta(hours=24)
        d = account.next_claim - now

        if (now - past).days >= 1:
            account.amount += 25
            account.next_claim = future
            account.save()
            await ctx.send(f'You claimed your daily! 25 has been credited to your account. Your new balance is: {account.amount}')
        else:
            print(f"You still have {d.seconds//3600} hour(s) before you can claim again.")
            return


# To add the bot to the cogs list
async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(EconomyBot(bot))
