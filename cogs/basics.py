#
# Simple commands that the user can use
#


import discord
from discord.ext import commands


class Basics(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.hybrid_command(name="ping",
                             description="Ping me!")
    async def ping(self, ctx):
        await ctx.send('Pong')

    @commands.command(name='say')
    async def say_prefix(self,
                         ctx: discord.ext.commands,
                         *,
                         message: str) -> None:
        await ctx.message.delete()
        await ctx.send(f'{message}')

    @discord.app_commands.command(name='say',
                                  description='Definitely make me say something yippe')
    async def say_slash(self,
                  ctx: discord.ext.commands,
                  *,
                  message: str) -> None:
        await ctx.response.send_message(f'{message}')


    @commands.hybrid_command(name="whoami",
                             brief="I tell you who I am",
                             description="I tell you who I am")
    async def whoami(self,
                     ctx: discord.ext.commands) -> None:
        await ctx.send(f'{ctx.message.author.mention}, I am **{self.bot.user.name}**. Just a simple dragon staring ' +
                       'into your soul.')


# To add the bot to the cogs list
async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Basics(bot))
