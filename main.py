#!/usr/bin/env python3

###########
# IMPORTS #
###########
from multiprocessing import Process
from website import run_flask
from discord_files.discord_app import run_discord


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

