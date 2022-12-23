"""
Practical Jokers
Gordon Mo, Ameer Alnasser, Ryan Lee
Softdev P01
2022-12-07
"""

import sqlite3

DB_FILE="back.db"

db=sqlite3.connect(DB_FILE, check_same_thread=False)
c = db.cursor()
db.executescript("""
CREATE TABLE if not exists jokes(user text, joke text);
CREATE TABLE if not exists userbase(user text, password text, country text, money int, highest int);
CREATE TABLE if not exists country(name text, current int, recent int);
CREATE TABLE if not exists dealercards(cardname text, cardname1 text, cardname2 text,cardname3 text,
    cardname4 text, cardname5 text, cardname6 text, cardname7 text, cardname8 text,
    cardname9 text, cardname10 text, cardname11 text,  total_value int);
CREATE TABLE if not exists playercards(cardname text, cardname1 text, cardname2 text,cardname3 text,
    cardname4 text, cardname5 text, cardname6 text, cardname7 text, cardname8 text,
    cardname9 text, cardname10 text, cardname11 text,  total_value int);
Insert into dealercards values('None','None','None','None','None','None','None','None','None','None','None','None',0);
Insert into playercards values('None','None','None','None','None','None','None','None','None','None','None','None',0);
""")
c.close()
#c = db.cursor()
#c.execute("select * from userbase")
#print(c.fetchall())
#c.close()
#Select column1,column2, from dealercard/playercard
#cursor fetchone
# get tuple
# for loop to check nones, then update cardnameN to card given
def add_country(name, current, recent):
    c=db.cursor()
    c.execute("Insert into country values(?,?,?)", (name, current, recent))
    c.close()

def user_exists(username):
    c=db.cursor()
    c.execute("Select user from userbase where user = ?", (username,))
    name = c.fetchone()
    c.close()
    return name and len(name) != 0

def add_joke(username, joke):
    c=db.cursor()
    c.execute("Insert into jokes values(?,?)", (username, joke))
    c.close()

def update_joke(username, joke):
    c=db.cursor()
    c.execute("UPDATE jokes SET joke = ? where user = ?", (joke, username))
    c.close()

def get_joke(username):
    c= db.cursor()
    c.execute("SELECT joke from jokes where user = ?", (username,))
    joke = c.fetchone()
    c.close()
    return joke

def add_user(username, password, country):
    c=db.cursor()
    if not user_exists(username):
        c.execute("Insert into userbase values(?,?,?,?,?)", (username, password, country, "1000", "1000"))
    db.commit()
    c.close()

def check_pass(username, password):
    c=db.cursor()

    # suername = ";; DROP table userbase;--"
    c.execute('select * from userbase where (user = ? )', (str(username), ))
    input_pass = c.fetchone()[1]
    c.close()
    return password == input_pass

def update_user_country(user_new,country_new):
    c=db.cursor()
    db.execute("UPDATE userbase Set country = ? where user=?", (str(country_new), str(user_new)))
    c.close()

def update_money_win(username, money_bet):
    c=db.cursor()
    c.execute("select money from userbase where user = ?", (username,))
    before_bet = c.fetchone()[0]
    c.close()
    c=db.cursor()
    after_bet = before_bet + money_bet
    c.execute("UPDATE userbase SET money = ? WHERE user =?", (after_bet, username))
    c.close()
    update_user_highest(username)
    update_country_money(get_user_country(username), money_bet)

def update_money_lose(username, money_bet):
    c=db.cursor()
    c.execute("select money from userbase where user = ?", (username,))
    before_bet = c.fetchone()[0]
    c.close()
    c=db.cursor()
    after_bet = before_bet - money_bet
    c.execute("UPDATE userbase SET money = ? WHERE user =?", (after_bet, username))
    c.close()
    update_country_money(get_user_country(username), money_bet)

def update_country_money(country, money_bet):
    c=db.cursor()
    c.execute("select current from country where name = ?", (country,))
    try:
        old_current = c.fetchone()[0]
        c.close()
        new_current = old_current + money_bet
    except:
        new_current = money_bet
    else:
        c=db.cursor()
        c.execute("UPDATE country SET current = ?, recent = ? where name = ?", (new_current, money_bet, country))
        c.close()

def get_user_country(username):
    c=db.cursor()
    c.execute("select country from userbase where user = ?", (username,))
    country = c.fetchone()[0]
    c.close()
    return country

def update_user_highest(username):
    c=db.cursor()
    c.execute("select highest, money from userbase where user = ?", (username,))
    output = c.fetchone()
    old_highest, money = output[0], output[1]
    print("money: ", money, "old_highest: ", old_highest)
    if(money > old_highest):
        c=db.cursor()
        c.execute("UPDATE userbase SET highest = ? where user = ?", (money, username))
        db.commit()
    c.close()


def add_player_card(value, card):
    c=db.cursor()
    #updates card
    c.execute("SELECT * FROM playercards")
    rows = c.fetchall()
    cards = list(rows[0])
    if "None" in rows[0]:
        cards.insert(0, card)
    cards.remove("None") # remove the first instance of None to replace with card
    reset_playercards()
    c.execute("UPDATE playercards SET cardname = ?, cardname1 = ?, cardname2 = \
    ?,cardname3 = ?, cardname4 = ?, cardname5 = ?, cardname6 = ?, cardname7 = ?\
    , cardname8 = ?, cardname9 = ?, cardname10 = ?, cardname11 = ?,  total_value\
     = ?", (cards[0],cards[1],cards[2],cards[3],cards[4],cards[5],cards[6],cards[7],cards[8],\
     cards[9],cards[10],cards[11],cards[12]))
    #updates value
    totalvalue = int(cards[12]) + int(value)
    c.execute("UPDATE playercards SET total_value = ?", (totalvalue,))
    c.close()

def add_dealer_card(value, card):
    c=db.cursor()
    #updates card
    c.execute("SELECT * FROM dealercards")
    rows = c.fetchall()
    cards = list(rows[0])
    if "None" in cards:
        cards.insert(0,card)
    cards.remove("None") # remove the first instance of None to replace with card
    reset_dealercards()
    c.execute("UPDATE dealercards SET cardname = ?, cardname1 = ?, cardname2 = ?,\
    cardname3 = ?, cardname4 = ?, cardname5 = ?, cardname6 = ?, cardname7 = ?, \
    cardname8 = ?, cardname9 = ?, cardname10 = ?, cardname11 = ?,  total_value = ?",
     (cards[0],cards[1],cards[2],cards[3],cards[4],cards[5],cards[6],cards[7],cards[8],cards[9],cards[10],cards[11],cards[12]))
    #updates value
    totalvalue = int(cards[12]) + int(value)
    c.execute("UPDATE dealercards SET total_value = ?", (totalvalue,))
    c.close()

def reset_playercards():
    c=db.cursor()
    c.execute("DROP TABLE IF EXISTS playercards;")
    c.execute("CREATE TABLE playercards(cardname text, cardname1 text, cardname2 text,cardname3 text, cardname4 text, cardname5 text, cardname6 text, cardname7 text, cardname8 text, cardname9 text, cardname10 text, cardname11 text,  total_value int);")
    c.execute("Insert into playercards values('None','None','None','None','None','None','None','None','None','None','None','None',0);")
    c.close()

def reset_dealercards():
    c=db.cursor()
    c.execute("DROP TABLE IF EXISTS dealercards;")
    c.execute("CREATE TABLE dealercards(cardname text, cardname1 text, cardname2 text,cardname3 text, cardname4 text, cardname5 text, cardname6 text, cardname7 text, cardname8 text, cardname9 text, cardname10 text, cardname11 text,  total_value int);")
    c.execute("Insert into dealercards values('None','None','None','None','None','None','None','None','None','None','None','None',0);")
    c.close()

def player_hand():
    c=db.cursor()
    c.execute("SELECT * FROM playercards")
    cards = c.fetchall()[0]
    c.close()
    return cards[:-1]

def dealer_hand():
    c=db.cursor()
    c.execute("SELECT * FROM dealercards")
    cards = c.fetchall()[0]
    c.close()
    return cards[:-1]

def display_card_list(hand):
    try:
        return hand.index("None")
    except ValueError:
        return -1

def get_player_value():
    c=db.cursor()
    c.execute("SELECT total_value FROM playercards")
    #print(c.fetchone[0])
    value = c.fetchone()[0]
    c.close()
    return value

def get_dealer_value():
    c=db.cursor()
    c.execute("SELECT total_value FROM dealercards")
    #print(c.fetchone[0])
    value = c.fetchone()[0]
    c.close()
    return value

def leaderboard_setup():
    c=db.cursor()
    c.execute("SELECT name, recent, current FROM country")
    rows = c.fetchall()
    c.close()
    return rows

def player_leaderboard_setup():
    c=db.cursor()
    c.execute("SELECT user,country,money,highest FROM userbase")
    leaders = c.fetchall()
    c.close()
    return leaders

def new_game():
    reset_playercards()
    reset_dealercards()

def num_ace_in_P():
    cards = player_hand()
    aces = cards.count("https://deckofcardsapi.com/static/img/aceDiamonds.png")
    aces += cards.count("https://deckofcardsapi.com/static/img/AC.png")
    aces += cards.count("https://deckofcardsapi.com/static/img/AH.png")
    aces += cards.count("https://deckofcardsapi.com/static/img/AS.png")
    return aces

def num_ace_in_D():
    cards=dealer_hand()
    aces = cards.count("https://deckofcardsapi.com/static/img/aceDiamonds.png")
    aces += cards.count("https://deckofcardsapi.com/static/img/AC.png")
    aces += cards.count("https://deckofcardsapi.com/static/img/AH.png")
    aces += cards.count("https://deckofcardsapi.com/static/img/AS.png")
    return aces

def better_val_function(hand):
    print("HAND: ", hand)
    vals = []
    for card in hand:
        if card != "None":
            vals.append(card[-6])
    vals = ['10' if v == 'J' or v == 'Q' or v == 'K' or v == '0' else '11' if v == 'A' or v == 'd' else v for v in vals]
    return sum(list(map(lambda x: int(x), vals)))

def sub_hand_ace_player(val, aces):
    real_val = better_val_function(player_hand())
    all_possible_values = []
    for i in range(aces+1):
        all_possible_values.append(real_val - 10*i)
    diff = list(map(lambda x: 21 - x if 21 - x >= 0 else 10000 + x, all_possible_values))
    print(f" val_arr: {all_possible_values} diff_array: {diff}")
    best_val = all_possible_values[diff.index(min(diff))]
    set_hand_val_player(best_val)
    return best_val == real_val, (best_val - real_val) // 10


def sub_hand_ace_dealer(val, aces):
    orig_aces = aces
    while val > 21 and aces > 0:
        val -= 10
        aces -=1
    set_hand_val_dealer(val)
    return orig_aces == aces, orig_aces - aces

def add_hand_ace_player(val, aces, times):
    set_hand_val_player(val + (10 * times))

def add_hand_ace_dealer(val, aces, times):
    set_hand_val_dealer(val + (10 * times))

def set_hand_val_player(value):
    c=db.cursor()
    c.execute("UPDATE playercards SET total_value = ?", (value,))
    c.close()

def set_hand_val_dealer(value):
    c=db.cursor()
    c.execute("UPDATE dealercards SET total_value = ?", (value,))
    c.close()

def balance_player(username):
    c=db.cursor()
    c.execute("select money from userbase where user = ?", (username,))
    balance = c.fetchone()[0]
    c.close()
    return balance

def hard_coded():
    add_user("aa","password","Canada")
