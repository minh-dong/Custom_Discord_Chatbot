# If it is first time setup, make sure to run this before running the main program!

import os

if __name__ == '__main__':
    # Create .env for the first time
    if os.path.exists(".env"):
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
