#
#
#


import discord
from discord.ext import commands
from palworld_server_management import invoke_pal_get_data, invoke_pal_save_world


class Palworld_Server_Management(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.hybrid_command(name="palserverinfo",
                             brief="Palworld Server info",
                             description="Get the current Palworld Server info")
    async def palserverinfo(self, ctx: discord.ext.commands):
        try:
            await ctx.send(f"Server info: {invoke_pal_get_data('info')}")
        except discord.HTTPException as err:
            await ctx.send('ERROR: Unable to retrieve information. Please see error report in terminal.')
            print(err)

    @commands.hybrid_command(name="palplayerlist",
                             brief="Palworld Server Player list",
                             description="Get the current Palworld Server Player list")
    async def palplayerlist(self, ctx: discord.ext.commands):
        try:
            await ctx.send(f"Server info: {invoke_pal_get_data('players')}")
        except discord.HTTPException as err:
            await ctx.send('ERROR: Unable to retrieve information. Please see error report in terminal.')
            print(err)

    @commands.hybrid_command(name="palserversettings",
                             brief="Palworld Server Settings",
                             description="Get the current Palworld Server Settings")
    async def palserversettings(self, ctx: discord.ext.commands):
        try:
            await ctx.send(f"Server info: {invoke_pal_get_data('settings')}")
        except discord.HTTPException as err:
            await ctx.send('ERROR: Unable to retrieve information. Please see error report in terminal.')
            print(err)

    @commands.hybrid_command(name="palservermetrics",
                             brief="Palworld Server Metrics",
                             description="Get the current Palworld Server Metrics")
    async def palservermetrics(self, ctx: discord.ext.commands):
        try:
            await ctx.send(f"Server info: {invoke_pal_get_data('metrics')}")
        except discord.HTTPException as err:
            await ctx.send('ERROR: Unable to retrieve information. Please see error report in terminal.')
            print(err)

    @commands.hybrid_command(name="palserversave",
                             brief="Palworld Server Save",
                             description="Save the world!")
    async def palserversave(self, ctx: discord.ext.commands):
        try:
            await ctx.send(f"Server info: {invoke_pal_save_world('save')}")
        except discord.HTTPException as err:
            await ctx.send('ERROR: Unable to save the world. Please see error report in terminal.')
            print(err)


# To add the bot to the cogs list
async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Palworld_Server_Management(bot))
