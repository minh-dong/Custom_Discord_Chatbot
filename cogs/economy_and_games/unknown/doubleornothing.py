#
# Double or Nothing. A 50/50 chance game.
#


import discord
from discord.ext import commands

from economy.models.account import Account
from economy.balance import updateAccountBalance

import asyncio
from random import choice

class DoubleOrNothing(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.hybrid_command(name="double",
                             brief="Want to double your points?",
                             description="Double your points or lose your bet!")
    async def double(self, ctx: discord.ext.commands, amount: int):
        # Get the user account
        account = Account.fetch(ctx.message)

        # Make sure the user has enough money in their account
        if amount > account.amount:
            await ctx.send(f"You don't have enough credits. Your balance is: {account.amount}")
            return

        # Welcome message as a message inside the Discord server
        await ctx.send('Welcome to Double or Nothing! You have a chance of ' +
                       'doubling your points or lose it all! Are you up for ' +
                       'the challenge? You can cancel this request by saying ' +
                       '**cancel**. Otherwise, wait 10 seconds before we reveal ' +
                       'if you doubled your provided points or not.\n\n' +
                       f'You are currently doubling {amount}.')

        # Get the response if we should continue or not
        while True:
            try:
                reply_message = await self.bot.wait_for('message', timeout=10)
            except asyncio.TimeoutError:
                break

            if reply_message.content == "cancel":
                return

        # 50/50 chance
        # False for lose
        # True for win
        winner: bool = choice([False, True])
        amount_pooled: int = amount

        if winner:
            amount_pooled *= 2
            await ctx.send(f'You win! {amount_pooled} will be credited to your account.')
        else:
            amount_pooled = 0
            await ctx.send(f'Oh no! You lost! You now have {account.amount}')

        # Update the account balance for the user
        updateAccountBalance(account, winner, amount_pooled)

        await ctx.send(f'You now have {account.amount}')


# To add the bot to the cogs list
async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(DoubleOrNothing(bot))
