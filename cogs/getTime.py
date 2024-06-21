#
# To get the current time
#

import discord
from discord.ext import commands
from datetime import datetime
import pytz
from pytz import timezone


class GetTime(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.utc = pytz.utc
        self.eastern = timezone('US/Eastern')
        self.format = "%Y-%m-%d %H:%M:%S %Z%z"

    @commands.hybrid_command(name="gettime",
                             brief="Get the time! Share the time!",
                             description="Get The time for any timezones. Default is US/Eastern",
                             aliases=["time", "whatisthetime"])
    async def ping(self, ctx, location: str = "US/Eastern"):
        #await ctx.send(f"The current time for this bot is {datetime.now().strftime('%H:%M:%S')} EST")
        if location in pytz.all_timezones:
            loc_dt = timezone(location)
            loc_time = loc_dt.localize(datetime.now())
            await ctx.send(f'The current time for {loc_dt.zone} is {loc_time.strftime(self.format)}')
        else:
            await ctx.send(f'You provided an invalid timezone! Please verify that you are inputting the correct timezone.')


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(GetTime(bot))
