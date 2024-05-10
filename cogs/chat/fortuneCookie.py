#
# A fortune cookie with predefined localized YAML dictionary
#


import discord
from discord.ext import commands

import chatbot


class FortuneCookie(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

#    @commands.Cog.listener()
#    async def on_message(self, message: discord.Message):
#        await message.add_reaction("❤️")

    @commands.hybrid_command(name="fortune",
                             brief="Fortune from a cookie",
                             description="Break a fortune cookie and I will read you your fortune!")
    async def fortune(self, ctx: discord.ext.commands):
        await ctx.send('Fortune cookie in progress')


# To add the bot to the cogs list
async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(FortuneCookie(bot))
