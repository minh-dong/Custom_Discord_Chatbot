import os


def get_guilds_text_file() -> str:
    file: str = os.path.dirname(__file__)
    return f"{file}\\..\\database\\guilds.txt"


def get_members_text_file() -> str:
    file: str = os.path.dirname(__file__)
    return f"{file}\\..\\database\\members.txt"
