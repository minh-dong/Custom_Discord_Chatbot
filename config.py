from urllib import parse

DISCORD_REDIRECT_URL="http://localhost:5000/oauth/callback"
DISCORD_OAUTH_URL=f"https://discord.com/oauth2/authorize?client_id=1228556083597934644&response_type=code&redirect_uri={parse.quote(DISCORD_REDIRECT_URL)}&scope=identify"
