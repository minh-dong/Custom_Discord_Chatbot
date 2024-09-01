from urllib import parse
from settings import PALWORLD_SERVER_URL

DISCORD_REDIRECT_URL="<Your redirect URL>"
DISCORD_OAUTH_URL=f"<Your OAUTH Url>_type=code&redirect_uri={parse.quote(DISCORD_REDIRECT_URL)}>"
PALWORLD_SERVER_URL=f"http://{PALWORLD_SERVER_URL}/v1/api/"
PALWORLD_SERVER_AUTH="<Your palworld server auth>"
