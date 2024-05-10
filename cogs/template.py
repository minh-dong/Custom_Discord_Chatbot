#
#
#


import discord
from discord.ext import commands


class XXCHANGENAMEXX(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

#    @commands.Cog.listener()
#    async def on_message(self, message: discord.Message):
#        await message.add_reaction("❤️")

#    @commands.hybrid_command(name="ping",
#                             brief="Ping me!",
#                             description="Ping me!")
#    async def ping(self, ctx: discord.ext.commands):
#        await ctx.send('Pong')


# To add the bot to the cogs list
async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(XXCHANGENAMEXX(bot))
