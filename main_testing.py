#!/usr/bin/env python3

###########
# IMPORTS #
###########
import discord
from discord.ext import commands
from discord import Intents, Client, Message
import os
#import dotenv
from dotenv import load_dotenv
from typing import Final, Literal, Optional
import random
from colorama import Back, Fore, Style
import platform
import time
import settings
from multiprocessing import Process

from website import run_flask

# Importing scripts made by me
import chatbot
import fortune_teller

# Admin stuff
from admin import load, unload, reload

# Variable to hold the json file that will be used in various defs
knowledge_base_json_file: str = 'chatbot/knowledge_base.json'





#class NotOwner(commands.CheckFailure):
#    ...


#def is_owner():
#    async def predicate(ctx):
#        if ctx.author.id != ctx.guild.owner_id:
#            raise NotOwner("Hey you are not the owner")
#        return True
#    return commands.check(predicate)


def run_discord() -> None:
    # Setting up the bot with commands and prefix and intents
    intents: Intents = Intents.default()
    intents.message_content = True  # NOQA
    intents.members = True # NOQA
    bot = commands.Bot(command_prefix='!', intents=intents, help_command=commands.DefaultHelpCommand())

    cogs_found: list = []

    @bot.event
    async def on_ready():
        for cog_file in settings.COGS_DIR.rglob("*.py"):
            #print(cog_file)
            temp_cog = str(cog_file).rsplit('cogs\\', maxsplit=1)[-1].replace('\\', '.')
            print(temp_cog)
            if not any(x in temp_cog for x in ["__init__.py", "template.py"]):
                # Save to a strong
                cogs_file: str = f"cogs.{temp_cog[:-3]}"

                # Append to the list
                cogs_found.append(cogs_file)

                # Load it into the cogs database
                await bot.load_extension(cogs_file)
        print(cogs_found)

        prfx = (Back.BLACK + Fore.GREEN + time.strftime("%H:%M:%S UTC",
                                                        time.gmtime()) + Back.RESET + Fore.WHITE + Style.BRIGHT)
        print(prfx + " Logged in as " + Fore.YELLOW + bot.user.name)
        print(prfx + " Bot ID " + Fore.YELLOW + str(bot.user.id))
        print(prfx + " Discord Version " + Fore.YELLOW + discord.__version__)
        print(prfx + " Python Version " + Fore.YELLOW + str(platform.python_version()))
        print(prfx + " Loading synced commands, please wait...")
        synced = await bot.tree.sync()
        print(prfx + " Slash CMDs Synced " + Fore.YELLOW + str(len(synced)) + " Commands")

        # For flask stuff website
        # Get the current status for all of the servers
        file = open('guilds.txt', 'w+')
        guilds = bot.guilds

        for guild in guilds:
            file.write(f'{guild.id}:{guild.name}\n')
        file.close()

        # Get the current status for all members within the servers
        members = bot.users
        file = open('members.txt', 'w+')

        for member in members:
            file.write(f'{member.id}:{member.name}\n')
        file.close()


        # Admin stuff
        # @todo - the cogs are not being found properly. will need to do something here.
        #         it is being called as appropiately, but it may be the "cog" not getting the right file name
        print(cogs_found)
        load(bot)
        unload(bot)
        reload(bot)

#    @bot.command(hidden=True)
#    @is_owner()
#    async def load(ctx, cog: str):
#        await bot.load_extension(f"cogs.{cog.lower()}")
#        await ctx.send(f"Successfully loaded **{cog}.py**")
#
#    @load.error
#    async def say_error(ctx, error):
#        if isinstance(error, NotOwner):
#            await ctx.send("Permission Denied")


#    @bot.command(hidden=True)
#    @is_owner()
#    async def unload(ctx, cog: str):
#        await bot.unload_extension(f"cogs.{cog.lower()}")
#        await ctx.send(f"Successfully unloaded **{cog}.py**")
#
#    @unload.error
#    async def say_error(ctx, error):
#        if isinstance(error, NotOwner):
#            await ctx.send("Permission Denied")

#    @bot.command(hidden=True)
#    @is_owner()
#    async def reload(ctx, cog: str):
#        await bot.reload_extension(f"cogs.{cog.lower()}")
#        await ctx.send(f"Successfully reloaded **{cog}.py**")
#
#    @reload.error
#    async def say_error(ctx, error):
#        if isinstance(error, NotOwner):
#            await ctx.send("Permission Denied")

    # # Reference: https://about.abstractumbra.dev/discord.py/2023/01/29/sync-command-example.html
    # @bot.command(hidden=True)
    # @commands.guild_only()
    # @is_owner()
    # async def sync(ctx: commands.Context,
    #                guilds: commands.Greedy[discord.Object],
    #                spec: Optional[Literal["~", "*", "&"]] = None) -> None:
    #     if not guilds:
    #         if spec == "~":
    #             synced = await ctx.bot.tree.sync(guild=ctx.guild)
    #         elif spec == "*":
    #             ctx.bot.tree.copy_global_to(guild=ctx.guild)
    #             synced = await ctx.bot.tree.sync(guild=ctx.guild)
    #         elif spec == "^":
    #             ctx.bot.tree.clear_commands(guild=ctx.guild)
    #             #await ctx.bot.tree.sync(guild=ctx.guild)
    #             synced = []
    #             await ctx.send('sync ^ involvked')
    #         else:
    #             synced = await ctx.bot.tree.sync()
    #
    #         await ctx.send(
    #             f"Synced {len(synced)} commands {'globally' if spec is None else 'to the current guild.'}"
    #         )
    #         return
    #
    #     ret = 0
    #     for guild in guilds:
    #         try:
    #             await ctx.bot.tree.sync(guild=guild)
    #         except discord.HTTPException:
    #             pass
    #         else:
    #             ret += 1
    #
    #     await ctx.send(f'Synced the tree to {ret}/{len(guilds)}.')
    #
    # @sync.error
    # async def say_error(ctx, error):
    #     if isinstance(error, NotOwner):
    #         await ctx.send("Permission Denied")

    # Run the bot with the secret API key
    bot.run(settings.DISCORD_API_SECRET)








# The main actual function for this entire script
if __name__ == '__main__':
    # Initialize the processes
    flask_process = Process(target=run_flask)
    discord_process = Process(target=run_discord)

    # Start the processes
    flask_process.start()
    discord_process.start()

    # Join the processes
    flask_process.join()
    discord_process.join()

