#
# To get the current time
#

import discord
from discord.ext import commands
from functools import wraps
from time import perf_counter, sleep


def get_time(func):
    """Times any function"""

    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = perf_counter()

        func(*args, **kwargs)

        end_time = perf_counter()

        total_time = round(end_time - start_time, 2)

        print('Time', total_time, 'seconds')

    return wrapper

@get_time
def do_something(param: str):
    """Does something important"""

    sleep(1)
    print(param)



def even_number():
    evens: list = []
    for number in range(50):
        is_even = number % 2 == 0
        if is_even:
            evens.append(number)

    return evens


class GetTime(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.hybrid_command(name="gettime", description="Get Time")
    async def ping(self, ctx):
        do_something('yay')
        print(do_something.__name__)
        print(do_something.__doc__)
        print(even_number())
        await ctx.send('Get time function in development')


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(GetTime(bot))
