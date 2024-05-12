import os

def get_economy_database_path() -> str:
    file: str = os.path.dirname(__file__)
    return f"{file}\\..\\database\\economy.db"


def get_discord_db_path() -> str:
    file: str = os.path.dirname(__file__)
    return f"{file}\\..\\database\\discord.db"
