# If it is first time setup, make sure to run this before running the main program!

import os

if __name__ == '__main__':
    # Create .env for the first time
    if not os.path.exists(".env"):
        with open(".env", "w") as file:
            file.write("DISCORD_TOKEN=<YOUR DISCORD TOKEN HERE>")
            file.write("DISCORD_CLIENT_SECRET=<YOUR DISCORD CLIENT SECRET CODE HERE>")
    else:
        print(".env file exists. Not creating...\n")

    # Create database/ directory for the first time
    try:
        os.mkdir("database")
    except OSError:
        print("database/ folder exist. Not creating...\n")

    # Let the user know about creating the requirements.txt for the first time
    print("Run the following command in your terminal: pip install -r requirements.txt")

    # Create the config.py file
    if not os.path.exists("config.py"):
        with open("config.py", "w") as file:
            file.write("from urllib import parse\n")
            file.write("\n")
            file.write("DISCORD_REDIRECT_URL=<YOUR REDIRECT URL>\n")
            file.write("DISCORD_OAUTH_URL=<YOUR OAUTH URL>\n")

    # Create the local_files directory
    try:
        os.mkdir("local_files")
    except OSError:
        print("local_files/ folder exist. Not creating...")
