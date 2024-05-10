#
# Randomly generate a number and display it to the user
#

import discord
from discord.ext import commands
import random


def random_numbers(num_max: int):
    # num_max in this range needs to add one because it will not yield at 20. We want the range to truly be 1-real max
    for i in range(1, num_max + 1):
        yield i


# TO use this code
# gen = generator()
# next(gen)
# or
# list(gen)
def generator(num_max: int):
    # get numbers from 1 to num_max
    yield from random_numbers(num_max)


# This will use the same logic as in the RNG.
def additional_generator(num_max: int):
    max_list_length: int = random.randrange(1, 100)

    some_number: list = []

    # Create the list based on the amount of numbers
    for x in range(0, max_list_length):
        some_number.append(random.randrange(1, num_max))

    return some_number


class RNG(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.hybrid_command(name='rng',
                        brief='Are you up for the RNGesus?',
                        description='Is RNG on your side?')
    async def rng(self, ctx, *, max_limit=20):
        #numbers_list: list = list(generator(max_limit))

        #some_number: list = additional_generator(max_limit)

        # Add the two lists together
        #some_number += numbers_list

        # A random number has been picked!
        #picked_number: int = random.choice(some_number)

        # Just generate a random number between a random range
        picked_number: int = random.randint(max_limit)

        if picked_number < (max_limit / 2):
            await ctx.send(f'Out of {max_limit}, you rolled a low number! --> {picked_number}')
        else:
            await ctx.send(f'Out of {max_limit}, you rolled a high number! --> {picked_number}')


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(RNG(bot))
