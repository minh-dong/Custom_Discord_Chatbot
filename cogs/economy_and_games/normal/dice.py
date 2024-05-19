#
#
#

import random
import asyncio
import discord
from discord.ext import commands

from economy.models.account import Account
from economy.balance import updateAccountBalance

class Dice(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.hybrid_command(name="dice",
                             brief="Roll a 6-sided dice!",
                             description="Roll a 6-sided dice!")
    async def ping(self, ctx: discord.ext.commands):
        # Get the account from the user
        account = Account.fetch(ctx.message)

        # cost to play
        amount = 50

        # Check if the user has enough
        if amount > account.amount:
            await ctx.send(f"You don't have enough credits. Your balance is: {account.amount}")
            return

        # Random numbers from 1 to 6
        winner_number: int = random.randint(1,6)
        random_number = random.randint(1, 6)

        await ctx.send(f'You rolled a {random_number}!\n' +
                        'Do you want to roll again or stay?\n' +
                        'Answer with: **yes** or **no**')

        # Get the confirmation of yes or no from the actual user
        while True:
            try:
                reply_message = await self.bot.wait_for('message', timeout=6)
            except asyncio.TimeoutError:
                await ctx.send(f"You did not reply so we are keeping your current roll of {random_number}")
                break

            # Only the user who replied can respond to the bot
            if ctx.message.author.id == reply_message.author.id:
                pass
            else:
                continue

            # Intrepert the user's message
            if reply_message.content == "yes":
                random_number = random.randint(1,6)
                await ctx.send(f"Your new roll is {random_number}.")
                break
            elif reply_message.content == "no":
                break

        # Bool for win/lose
        did_user_win: bool = False

        # See the winner number of the 6-sided dice
        if winner_number == random_number:
            did_user_win = True
            await ctx.send(f"Your {random_number} matches the winning number {winner_number}!")
        else:
            await ctx.send(f"Your {random_number} did not match the winning number {winner_number}!")

        # Update the balance
        updateAccountBalance(account, did_user_win, amount)

        # Give the user coins
#        if did_user_win:
#            account.amount += 50
#        else:
#            account.amount -= 50

        # Save the account
#        account.save()

        # Send the message
        await ctx.send(f"Your new balance is {account.amount}. Thank you for playing!")


# To add the bot to the cogs list
async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Dice(bot))
