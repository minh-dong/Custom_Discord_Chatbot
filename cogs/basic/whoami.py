#
# Get the current user who used this command to @ them and then say who this bot is.
#

import discord
from discord.ext import commands


class Whoami(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.hybrid_command(name="whoami",
                             brief="I tell you who I am",
                             description="I tell you who I am")
    async def whoami(self, ctx: discord.ext.commands) -> None:
        await ctx.send(f'{ctx.message.author.mention}, I am **{self.bot.user.name}**. Just a simple dragon staring ' +
                       'into your soul.')


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Whoami(bot))
