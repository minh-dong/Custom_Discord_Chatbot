from random_word import RandomWords
import yaml
from random import choice
import os

# @todo - need to update this function to allow detection of easy, normal, etc
#         difficulties. cogs will also be updated to reflect this change.
def generateRandomWord() -> str:
    # Variable to get the file name
    file_words = f"{os.path.dirname(__file__)}\\words.yaml"

    # Load the yaml file into a dictionary
    with open(file_words, "r", encoding="utf8") as file:
        try:
            data = yaml.safe_load(file)
        except yaml.YAMLError as err:
            print(err)

    #print(data.items())
    #print(data.get("easy"))

    #print(data.get("easy"))
    #print([RandomWords().get_random_word()])
    use_word = choice(data.get("easy") + [RandomWords().get_random_word()])

    return str(use_word)
