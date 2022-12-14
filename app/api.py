"""
Practical Jokers
Softdev P01
2022-12-07
"""

import requests

list_of_countries = {"USA": "USD", "Canada":"CAD", "United Kingdom":"GBP"}

def joke():
    text = requests.get("https://v2.jokeapi.dev/joke/Any?blacklistFlags=nsfw,religious,political,racist,sexist,explicit&type=single")
    json = text.json()
    return json["joke"]

def get_deck_id():#gives the id of a new deck
    url = "https://deckofcardsapi.com/api/deck/new/shuffle/"
    req = requests.get(url, params={"deck_count": 1})#can change this later to be 6 decks for typical game of blackjack
    dictionary = req.json()
    return dictionary["deck_id"]

def draw1(deck_id):#draws once card from deck and returns tuple of value and image both strings
    url = "https://deckofcardsapi.com/api/deck/" + deck_id + "/draw/"
    req = requests.get(url, params={"count": 1})
    dictionary = req.json()
    return dictionary["cards"][0]["value"], dictionary["cards"][0]["images"]["png"]

def draw2(deck_id):#draws once card from deck and returns tuple of both card value and image all strings. Will be called to create first hand.
    url = "https://deckofcardsapi.com/api/deck/" + deck_id + "/draw/"
    req = requests.get(url, params={"count": 2})
    dictionary = req.json()
    return dictionary["cards"][0]["value"], dictionary["cards"][0]["images"]["png"],dictionary["cards"][1]["value"], dictionary["cards"][1]["images"]["png"]

# def reset(deck_id):#start a new round of blackjack
#     url = "https://deckofcardsapi.com/api/deck/" + deck_id + "/shuffle/"
#     req = requests.get(url)
#     return

def get_exchange(country1, country2, amt):
    key = open("keys\\key_exchangeRate.txt").read()
    currency1 = get_currency(country1)
    currency2 = get_currency(country2)
    url = "https://v6.exchangerate-api.com/v6/" + key + "/pair/" + currency1 +"/"+ currency2 +"/" + str(amt)
    #print(url)
    req = requests.get(url)
    json = req.json()
    converted = int(json["conversion_result"])
    return converted

def get_currency(country):
    return(list_of_countries[country])

print(get_currency("Canada"))
print(get_exchange("USA", "Canada", 100))

#deckid = get_deck_id()
#print(deckid)
#print(draw1(deckid))
#print(draw2(deckid))
#reset(deckid)