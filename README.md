# Custom Discord Chatbot
A custom Discord bot created in Python 3.12+ using discord.py <br/>
 
Project started on April 1st 2024. <br/>

# What is this project about?
This project is a self-learning process utilizing Discord API and trying out different
APIs, packages, and more. <br/>
 
Various bot commands are at the user's disposal when the bot is inside the Discord
server. <br/>

# How to run
This project will only work in Python 3.12 and beyond. Please make sure to have Python 3.12 installed on your system.<br>
<br>

> [!NOTE]
> Project was built on Windows 11. May or may not work for Linux (haven't tested it yet)

1) Ensure that Python 3.12 is installed on your system
2) Run the setup.py
3) Run the following command in the terminal: pip install -r requirements.txt
4) [OPTIONAL] If you do not need a dashboard, comment out lines related to "flask" in the main.py
5) Run main.py
 
# Current working commands
!ping - Pong <br/>
!whoami - Bot am I? <br/>
!say [message] - The bot will say exactly what you want it to say <br/>
!fortune - Get a random fortune from the list. Bad to good. <br/>
!chat [message] - Chat with the bot! <br/>
!rng - Will random number generator be in your favor? <br/>
!gettime [location : str value] | !time [location : str value] | !whatisthetime [location : str value] - Will get the current time for the bot <br/>

# Economy System
The economy is a balance system in any Discord server. All information and balance is stored in a SQL database 
utilizing SQLite. All newly added users will start with a balance of **0 credits** and must use the following 
**!claim** command to receive their daily credits.

## Current Commands for User's Economy Info
!claim - Get your daily claim of 25 points (24 hour timer) <br/>
!balance | !bal | !money - Get your current balance <br/>

## Games
!coin [h | t] [bal : integer value] <br/>
!palindrome <br>
!dice <br>
!double [amount : integer value] <br>
!blackjack <br>
