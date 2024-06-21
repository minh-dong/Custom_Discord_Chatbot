#
# A minigame where you need to get to 21 or at least be higher than the dealer
#


import discord
from discord.ext import commands
import asyncio

from random import choice

from economy.models.account import Account
from economy.balance import updateAccountBalance


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


class Blackjack(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.cards = ['A', '2', '3', '4', '5', '6',
                      '7', '8', '9', '10', 'J', 'Q', 'K',]

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
                        reply_message = 'Stand'
                        break

                    # Make sure that only the user is replying and nobody else.
                    if ctx.message.author.id == reply_message.author.id:
                        pass
                    else:
                        continue

                    # for reply messages and when to break
                    if reply_message.content.lower() in ['hit', 'h']:
                        break
                    elif reply_message.content.lower() in ['stand', 's']:
                        break
                    else:
                        await ctx.send('Please respond appropriately to the prompt\n' +
                                       f'{player_message}')
            else:
                reply_message = 's'

            # Check for some conditions
            if value_player > 21:
                player_message = 'BUST!'
                bust_player = True
                turn_player = False
                turn_dealer = True
            elif value_player < 21 and reply_message.content.lower() in ['hit', 'h']:
                # if hit, draw a new card from the deck
                hand_player.append(choice(self.cards))
            elif reply_message.content.lower() in ['stand', 's']:
                turn_player = False
                turn_dealer = True

        # It's the dealer's turn
        while turn_dealer:
            # Evaluate the dealer's hand
            value_dealer: int = card_conversion(hand=hand_dealer)

            if value_dealer > 21:                          # Automatically stand above 16
                dealer_message = 'Dealer busted.\n'
                turn_dealer = False
                bust_dealer = True
            elif value_dealer == 21:                       # Auto wins for dealer at 21
                dealer_message = 'Dealer has 21. You lose.\n'
                turn_dealer = False
            elif value_dealer > 18:                        # Auto stands for dealer above 18
                dealer_message = 'Dealer is going to stand.\n'
                turn_dealer = False
            elif value_dealer <= 18:                       # Continue to draw below value of 18
                hand_dealer.append(choice(self.cards))
                continue

            # Nicely formatted string
            hand_dealer_nicely_formatted: str = ' '.join(hand_dealer)

            # Send a message to the chat
            await ctx.send(f"Dealer's hand: {hand_dealer_nicely_formatted}.\n {dealer_message}")

        # Calculate who wins
        if value_dealer == 21:                      # Auto wins for dealer, lose
            winner = False
        elif value_player <= 21 and bust_dealer:    # if player is 21 or less and dealer busted, win
            winner = True
        elif value_player > value_dealer:           # if value of player is greater than dealer, win
            winner = True
        elif bust_player:                           # if player bust, lose
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


# To add the bot to the cogs list
async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Blackjack(bot))
