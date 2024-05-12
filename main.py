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

# For database
from economy.models.account import Account
#import database
from economy import get_economy_database

#discord_files
from discord_files.discord_text_files import get_guilds_text_file, get_members_text_file

def run_discord() -> None:
    # Economy database
    #database.db.create_tables([Account])
    get_economy_database().create_tables([Account])

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
        file = open(get_guilds_text_file(), 'w+')
        guilds = bot.guilds

        for guild in guilds:
            file.write(f'{guild.id}:{guild.name}\n')
        file.close()

        # Get the current status for all members within the servers
        members = bot.users
        file = open(get_members_text_file(), 'w+')

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

