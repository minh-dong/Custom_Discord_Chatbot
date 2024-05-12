import peewee
import os
from discord_files import get_economy_database_path


def get_economy_database() -> peewee.SqliteDatabase:
    # Get the database location
    file: str = get_economy_database_path()

    print("Database for economy: ", file)

    # Return the database
    return peewee.SqliteDatabase(file)
