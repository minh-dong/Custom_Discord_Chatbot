#
# Take exactly what the user put in the paramter and deletes their message (if used the !say) and say exactly what
# they said
#

import discord
from discord.ext import commands


class Say(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.command(name='say')
    async def say_prefix(self,
                         ctx: discord.ext.commands,
                         *,
                         message: str) -> None:
        await ctx.message.delete()
        await ctx.send(f'{message}')

    @discord.app_commands.command(name='say',
#                                  brief='Make me say something!',
                                  description='Definitely make me say something yippe')
    async def say_slash(self,
                  ctx: discord.ext.commands,
                  *,
                  message: str) -> None:
#        await ctx.message.delete()
        await ctx.response.send_message(f'{message}')


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Say(bot))
