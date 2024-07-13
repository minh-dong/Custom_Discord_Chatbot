# A simple function to get all the cogs

from os.path import dirname
from glob import glob


def get_main_dir_cogs() -> str:
    return dirname(__file__) + '\\..\\cogs\\'


def get_all_cogs() -> list:
    dir_cogs: str = get_main_dir_cogs()

    available_cogs: list = []

    temp: str
    final_input: str

    for filename in glob(dir_cogs + '**\\*.py', recursive=True):
        temp = filename.rsplit('\\', maxsplit=1)[-1]
        if temp not in ['template.py', '__init__.py']:
            final_input = 'cogs.' + filename.rsplit('\\cogs\\', maxsplit=1)[-1].replace('\\', '.').replace('.py', '')
            available_cogs.append(final_input)

    del temp, final_input

    return available_cogs


def find_cog(cog_lookup: str, item_list: list):
    for item in item_list:
        if cog_lookup == item.rsplit('.', maxsplit=1)[-1]:
            return item
