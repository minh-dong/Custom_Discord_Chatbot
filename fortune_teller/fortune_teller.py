import random

# @todo - Need to change this to utilize Flask? Not sure how to proceed yet
def get_fortune() -> str:
    # Dictionary to keep a bunch of different fortunes
    fortunes: dict = {
        "bad": {
            1: "EY. YOU STINK! No really, I predict a bad fortune and this is it.",
            2: "Bad luck strikes you for seven years. No wait, MEOW!",
            3: "Bad to the... no, bad person. Bad luck.",
            4: "You have reached a bad fortune. Try again!",
            5: "ERROR: Fortune not found."
        },
        "neutral": {
            1: "WARNING: Fortune found but it is illegible. But I have to say, it's a good fortune. Trust me.",
            2: "Hazy Reply. Please try again!"
        },
        "good": {
            1: "Yes.",
            2: "Definitely.",
            3: "You are the best person ever.",
            4: "You're beautiful.",
        },
        "godly": {
            1: "Did I say... be a god? Because you are a god! God out of this world! *chuckles*",
            2: "You are not 100% today. You're 200%! That means you are doubly awesome!.",
            3: "Say, how about a drink? Luck drink? 1000+ Luck has been added to your stats permanently.",
            4: "Luck over 9000. That means you are a **God at Luck**"
        }
    }

    # Pick one from the first gen keylist
    fortune_type: list = list(fortunes.keys())

    # Return a random fortune
    return random.choice(list(fortunes[random.choice(fortune_type)].values()))
