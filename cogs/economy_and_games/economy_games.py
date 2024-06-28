#
#
#


import discord
from discord.ext import commands
import random
import asyncio

from economy.games.palindrome.isPalindrome import isPalindrome
from economy.games.palindrome.generateRandomWord import generateRandomWord

from economy.models.account import Account
from economy.balance import updateAccountBalance

from datetime import datetime, timedelta

from random import choice


def card_conversion(hand: list) -> int:
    value: int = 0
    card_Ace: bool = False

    for item in hand:
        if item.isdigit():
            value += int(item)
        elif item == 'A':
            card_Ace = True
        elif item in ['J', 'Q', 'K']:
            value += 10

        if card_Ace:
            card_Ace = False

            if (value + 11) > 21:
                value += 1
            else:
                value += 11

    return value

class EconomyGames(commands.Cog):
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
            await ctx.send(
                f'You claimed your daily! 25 has been credited to your account. Your new balance is: {account.amount}')
        else:
            print(f"You still have {d.seconds // 3600} hour(s) before you can claim again.")
            return


    @commands.hybrid_command(name="coinflip",
                             brief="Coin flip with heads or tails!",
                             description="Coin flip with heads or tails to win/lose money!")
    async def coinflip(self, ctx, choice: str, amount: int):
        account = Account.fetch(ctx.message)

        if amount > account.amount:
            await ctx.send("You don't have enough credits.")
            return

        heads = random.randint(0, 1)

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
        # word = RandomWords().get_random_word()
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

        # Update the account balance
        updateAccountBalance(account, winner, amount)

        # Give the user some points
        #        if winner is True:
        #            account.amount += amount
        #        else:
        #            account.amount -= amount

        # Save the account
        #        account.save()

        # Send the message
        # @todo - ping the user
        await ctx.send(f"{message}\nYour new balance is {account.amount}")

    @commands.hybrid_command(name="blackjack",
                             brief="Beat the dealer or don't bust over 21!",
                             description="Beat the dealer or don't bust over 21!")
    async def ping(self, ctx: discord.ext.commands):
        # Get the account from the user
        account = Account.fetch(ctx.message)

        # cost to play
        amount = 50

        # Check if the user has enough
        if amount > account.amount:
            await ctx.send(f"You don't have enough credits. Your balance is: {account.amount}")
            return

        # Dealer's hand
        hand_dealer = [choice(self.cards), choice(self.cards)]

        # Player's hand
        hand_player = [choice(self.cards), choice(self.cards)]

        # Extra variables
        winner = False
        hand_player_first_draw = True
        turn_player = True
        turn_dealer = False
        value_player: int = 0
        value_dealer: int = 0
        bust_player: bool = False
        bust_dealer: bool = False
        turn_player_autostand: bool = False

        # It's the player's turn
        while turn_player:
            # Evaluate the player's hand
            value_player: int = card_conversion(hand=hand_player)

            # Automatically stand on 21
            if value_player == 21 and hand_player_first_draw:
                hand_player_first_draw = False
                player_message: str = "Blackjack! Let's see if you beat your opponent's hand. . .\n"
                turn_player = False
                turn_dealer = True
            elif value_player == 21 and not hand_player_first_draw:
                player_message: str = "You reached 21! Let's see if you beat your opponent's hand. . .\n"
                turn_player = False
                turn_dealer = True
            else:
                player_message: str = ("Hit or Stand? (please type Hit or H for hit, Stand or S for stand). You will " +
                                       "automatically stand if you do not reply in 60s.\n")

            # Change the list to a string instead
            # @todo
            hand_player_nicely_formatted: str = ' '.join(hand_player)

            # Send a message to the chat
            await ctx.send(f"Dealer's hand: {hand_dealer[0]}, ???\n" +
                           f"Your hand: {hand_player_nicely_formatted}\n\n" +
                           player_message)

            # If we are already at 21, we no longer need to wait for the user's prompt
            if turn_player:
                # Get the response from the user
                while True:
                    try:
                        reply_message = await self.bot.wait_for('message', timeout=60)
                    except asyncio.TimeoutError:
                        await ctx.send(f"You did not reply so you are automatically going to stand")
                        # reply_message = 'Stand'
                        turn_player_autostand = True
                        break

                    # Make sure that only the user is replying and nobody else.
                    if ctx.message.author.id == reply_message.author.id:
                        pass
                    else:
                        continue

                    # for reply messages and when to break
                    if reply_message.content.lower() in ['hit', 'h']:
                        break
                    elif reply_message.content.lower() in ['stand', 's'] or turn_player_autostand:
                        break
                    else:
                        await ctx.send('Please respond appropriately to the prompt\n' +
                                       f'{player_message}')
            else:
                turn_player_autostand = True

            # Check for some conditions
            if value_player > 21:
                player_message = 'BUST!'
                bust_player = True
                turn_player = False
                turn_dealer = True
            elif value_player < 21 and reply_message.content.lower() in ['hit', 'h']:
                # if hit, draw a new card from the deck
                hand_player.append(choice(self.cards))
            elif reply_message.content.lower() in ['stand', 's'] or turn_player_autostand:
                turn_player = False
                turn_dealer = True

        # It's the dealer's turn
        while turn_dealer:
            # Evaluate the dealer's hand
            value_dealer: int = card_conversion(hand=hand_dealer)

            if value_dealer > 21:  # Automatically stand above 16
                dealer_message = 'Dealer busted.\n'
                turn_dealer = False
                bust_dealer = True
            elif value_dealer == 21:  # Auto wins for dealer at 21
                dealer_message = 'Dealer has 21. You lose.\n'
                turn_dealer = False
            elif value_dealer > 18:  # Auto stands for dealer above 18
                dealer_message = 'Dealer is going to stand.\n'
                turn_dealer = False
            elif value_dealer <= 18:  # Continue to draw below value of 18
                hand_dealer.append(choice(self.cards))
                continue

            # Nicely formatted string
            hand_dealer_nicely_formatted: str = ' '.join(hand_dealer)

            # Send a message to the chat
            await ctx.send(f"Dealer's hand: {hand_dealer_nicely_formatted}.\n {dealer_message}")

        # Calculate who wins
        if value_dealer == 21:  # Auto wins for dealer, lose
            winner = False
        elif value_player <= 21 and bust_dealer:  # if player is 21 or less and dealer busted, win
            winner = True
        elif value_player > value_dealer:  # if value of player is greater than dealer, win
            winner = True
        elif bust_player:  # if player bust, lose
            winner = False

        # Final amount x 2 if win, else lose 50
        if winner:
            amount_final = amount * 2
        else:
            amount_final = amount

        # Update the account balance accordingly
        updateAccountBalance(account=account, winner=winner, amount=amount_final)

        # Send the message
        await ctx.send(f"Your new balance is {account.amount}. Thank you for playing!")

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
        winner_number: int = random.randint(1, 6)
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
                random_number = random.randint(1, 6)
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
            amount_pooled = amount
            await ctx.send(f'Oh no! You lost! You now have {account.amount}')

        # Update the account balance for the user
        updateAccountBalance(account, winner, amount_pooled)

        await ctx.send(f'You now have {account.amount}')


# To add the bot to the cogs list
async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(EconomyGames(bot))
