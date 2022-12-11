"""
Practical Jokers
Softdev P01
2022-12-07
"""

import requests

def joke():
    text = requests.get("https://v2.jokeapi.dev/joke/Any?blacklistFlags=nsfw,religious,political,racist,sexist,explicit&type=single")
    json = text.json()
    return json["joke"]