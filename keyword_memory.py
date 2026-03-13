import json
import os

FILE = "keywords.json"


def save_keywords(keywords):

    with open(FILE, "w") as f:
        json.dump(keywords, f, indent=4)


def load_keywords():

    if not os.path.exists(FILE):
        return None

    with open(FILE) as f:
        return json.load(f)