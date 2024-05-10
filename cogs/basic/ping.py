#
# The simple ping command with the response of pong
#

import discord
from discord.ext import commands


class Ping(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

#    @commands.Cog.listener()
#    async def on_message(self, message: discord.Message):
#        await message.add_reaction("❤️")

    @commands.hybrid_command(name="ping", description="Ping me!")
    async def ping(self, ctx):
        await ctx.send('Pong')


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Ping(bot))
