#
# Cats cats cats! Gotta get them cats meowing!
#
# Link: https://cataas.com/
#


import discord
from discord.ext import commands

import requests


class Cat(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

        # Static URL
        self.url: str = 'https://cataas.com/'

        # additional url
        self.cat: str = 'cat'

        # @todo - NOT YET IMPLEMENTED
        # Additional urls for customization and such
        self.tag: str = '<tags>'
        self.gif: str = 'gif'
        self.say: str = '/says/<txt>'
        self.tagsay: str = 'cat/<tags>/says/<txt>'
        self.sayfontcolor: str = 'cat/says/<txt?fontSize=:size&fontColor=:color>'

    @commands.hybrid_command(name="cat",
                             brief="Get a cat picture!",
                             description="Cats are everywhere! Meow!")
    async def ping(self, ctx: discord.ext.commands):
        item: str = self.url + self.cat
        r: requests = requests.get(item)
        await ctx.send(r.url)


# To add the bot to the cogs list
async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Cat(bot))
