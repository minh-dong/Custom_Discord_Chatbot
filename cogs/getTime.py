#
# To get the current time
#

import discord
from discord.ext import commands
from datetime import datetime


class GetTime(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.hybrid_command(name="gettime", description="Get Time")
    async def ping(self, ctx):
        await ctx.send(f"The current time for this bot is {datetime.now().strftime('%H:%M:%S')} EST")


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(GetTime(bot))
