import peewee
import os
from discord_files import get_economy_database_path


def get_economy_database() -> peewee.SqliteDatabase:
    # Get the database location
#    location: str = os.path.dirname(__file__)
#    file: str = location + "\\..\\database\\economy.db"
    file: str = get_economy_database_path()

    print("Database for economy: ", file)

    # Return the database
    return peewee.SqliteDatabase(file)
