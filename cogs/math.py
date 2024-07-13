#
# Math related stuff
#


import discord
from discord.ext import commands
import random


class Math(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.hybrid_command(name='rng',
                             brief='Are you up for the RNGesus?',
                             description='Is RNG on your side?')
    async def rng(self, ctx, *, dice=20):
        # Just generate a random number between a random range
        picked_number: int = random.randint(1, dice)

        if picked_number < (dice / 2):
            await ctx.send(f'Out of {dice}, you rolled a low number! --> {picked_number}')
        else:
            await ctx.send(f'Out of {dice}, you rolled a high number! --> {picked_number}')


# To add the bot to the cogs list
async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Math(bot))
