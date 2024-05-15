#
# Palindrome is to determine a random string from a json file and the user will have to say yes or not to determine
# if it is a valid palindrome or not.
#
# Random-Word python library
# https://pypi.org/project/Random-Word/

import discord
from discord.ext import commands
import asyncio
from random_word import RandomWords

from economy.games.palindrome.isPalindrome import isPalindrome
from economy.games.palindrome.generateRandomWord import generateRandomWord

from economy.models.account import Account


class Palindrome(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.hybrid_command(name="palindrome",
                             brief="Am I the same forward and back?",
                             description="Is my text the same forward and backwards?")
    async def palindrome(self, ctx: discord.ext.commands):
        # Get the author
        author = ctx.message.author

        # Fetch the account
        account = Account.fetch(ctx.message)

        # Check if user has enough money
        amount = 10
        if amount > account.amount:
            await ctx.send(f"You don't have enough credits. Your balance is: {account.amount}")
            return

        # Get the random word to use for the palindrome game
        #word = RandomWords().get_random_word()
        word: str = generateRandomWord()

        # Send the message to the discord server
        # @todo - ping the user
        await ctx.send("Hello!. Welcome to palindrome game!\n" +
                       f"The first word will be **{word}**\n" +
                       "You have 15 seconds. Please say **yes** or **no**")

        # Variables
        winner: bool = False
        message: str = ''

        # A while loop mainly for the invalid responses. The user musr say yes or no
        # @todo - need to fix this so timeout remembers the last timeout timer
        while True:
            try:
                reply_message = await self.bot.wait_for('message', timeout=15)
            except asyncio.TimeoutError:
                await ctx.send("You ran out of time!")

            bool_palindrome = isPalindrome(word)

            # Make sure the bot only replies in the same channel
            if ctx.channel.id == reply_message.channel.id:
                pass
            else:
                continue

            # Only the user who replied can respond to the bot
            if ctx.message.author.id == reply_message.author.id:
                pass
            else:
                continue

            # Get the user's message
            if reply_message.content == 'yes':
                if bool_palindrome:
                    message = f"You win! **{word}** is a palindrome!"
                    winner = True
                    break
                else:
                    message = f"You lose! **{word}** is a palindrome!"
                    break
            elif reply_message.content == 'no':
                if not bool_palindrome:
                    message = f"You win! **{word}** is NOT a palindrome!"
                    winner = True
                    break
                else:
                    message = f"You lose! **{word}** is NOT a palindrome!"
                    break
            else:
                await ctx.send("INVALID CHOICE! Please reply with **yes** or **no**")

        # Give the user some points
        if winner is True:
            account.amount += amount
        else:
            account.amount -= amount

        # Save the account
        account.save()

        # Send the message
        # @todo - ping the user
        await ctx.send(f"{message}\nYour new balance is {account.amount}")


# To add the bot to the cogs list
async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Palindrome(bot))
