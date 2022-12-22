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
CREATE TABLE if not exists consoomer(user text, password text, country text, money int);
CREATE TABLE if not exists dabloons(country text, highest real, current real, recent real);
CREATE TABLE if not exists country(country text, GDP int);
CREATE TABLE if not exists dealercards(cardname text, cardname1 text, cardname2 text,cardname3 text,
    cardname4 text, cardname5 text, cardname6 text, cardname7 text, cardname8 text,
    cardname9 text, cardname10 text, cardname11 text,  total_value int);
CREATE TABLE if not exists playercards(cardname text, cardname1 text, cardname2 text,cardname3 text,
    cardname4 text, cardname5 text, cardname6 text, cardname7 text, cardname8 text,
    cardname9 text, cardname10 text, cardname11 text,  total_value int);
Insert into dealercards values('None','None','None','None','None','None','None','None','None','None','None','None',0);
Insert into playercards values('None','None','None','None','None','None','None','None','None','None','None','None',0);
Insert into consoomer values(?,?,?,?), ('aa', 'password', 'USA', '1000');
Insert into country values("USA", 10000);
""")
c.close()
#c = db.cursor()
#c.execute("select * from consoomer")
#print(c.fetchall())
#c.close()
#Select column1,column2, from dealercard/playercard
#cursor fetchone
# get tuple
# for loop to check nones, then update cardnameN to card given

def user_exists(username):
    c=db.cursor()
    c.execute("Select user from consoomer where user = ?", (username,))
    try:
        c.fetchone()[0]==username
        c.close()
        return True
    except: #If c.fetchone does not have an entry, then we want to catch the error and return an exception
        c.close()
        return False

def add_user(username, password, country):
    c=db.cursor()
    c.execute("Insert into consoomer values(?,?,?,?)", (username, password, country, "1000"))
    c.close()

def check_pass(username, password):
    c=db.cursor()
    c.execute('select * from consoomer where (user = ? AND password = ?)', (str(username), str(password)))
    try:
        c.fetchone()[0]
        c.close()
        return True
    except:
        c.close()
        return False

def update_country(user_new,country_new):
    c=db.cursor()
    db.execute("UPDATE consoomer Set country = ? where user=?", (str(country_new), str(user_new)))
    c.close()

def update_money_win(username, money_bet):
    c=db.cursor()
    c.execute("select money from consoomer where user = ?", (username,))
    before_bet = c.fetchone()
    after_bet = before_bet[0] + money_bet
    c.execute("UPDATE consoomer SET money = after_bet WHERE user =?", (username,))
    c.close()

def update_money_lose(username, money_bet):
    c=db.cursor()
    c.execute("select money from consoomer where user = ?", (username,))
    before_bet = c.fetchone()
    after_bet = before_bet[0] - money_bet
    c.execute("UPDATE consoomer SET money = after_bet WHERE user =?", (username,))
    c.close()

def add_player_card(value, card):
    c=db.cursor()
    #updates card
    c.execute("SELECT * FROM playercards")
    rows = c.fetchall()
    lst = []
    added = False
    for i in range(len(rows[0])):
        if(rows[0][i] == 'None' and added == False):
            lst.append(card)
            added = True
        elif(rows[0][i] != 'None' or added == True):
            lst.append(rows[0][i])
    totalvalue = int(lst[12])
    reset_playercards()
    c.execute("UPDATE playercards SET cardname = ?, cardname1 = ?, cardname2 = ?,cardname3 = ?, cardname4 = ?, cardname5 = ?, cardname6 = ?, cardname7 = ?, cardname8 = ?, cardname9 = ?, cardname10 = ?, cardname11 = ?,  total_value = ?", (lst[0],lst[1],lst[2],lst[3],lst[4],lst[5],lst[6],lst[7],lst[8],lst[9],lst[10],lst[11],lst[12]))
    #updates value
    totalvalue += int(value)
    c.execute("UPDATE playercards SET total_value = ?", (totalvalue,))
    c.close()

def add_dealer_card(value, card):
    c=db.cursor()
    #updates card
    c.execute("SELECT * FROM dealercards")
    rows = c.fetchall()
    lst = []
    added = False
    for i in range(len(rows[0])):
        if(rows[0][i] == 'None' and added == False):
            lst.append(card)
            added = True
        elif(rows[0][i] != 'None' or added == True):
            lst.append(rows[0][i])
    totalvalue = int(lst[12])
    reset_dealercards()
    c.execute("UPDATE dealercards SET cardname = ?, cardname1 = ?, cardname2 = ?,cardname3 = ?, cardname4 = ?, cardname5 = ?, cardname6 = ?, cardname7 = ?, cardname8 = ?, cardname9 = ?, cardname10 = ?, cardname11 = ?,  total_value = ?", (lst[0],lst[1],lst[2],lst[3],lst[4],lst[5],lst[6],lst[7],lst[8],lst[9],lst[10],lst[11],lst[12]))
    #updates value
    totalvalue += int(value)
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
    rows = c.fetchall()
    lst = []
    for item in rows[0]:
        lst.append(item)
    lst.pop()
    c.close()
    return lst

def dealer_hand():
    c=db.cursor()
    c.execute("SELECT * FROM dealercards")
    rows = c.fetchall()
    lst = []
    for item in rows[0]:
        lst.append(item)
    lst.pop()
    c.close()
    return lst

def display_card_list(hand):
    index_of_none = -1
    for i in range(len(hand)):
        if hand[i] == "None":
            index_of_none = i
            break

    return index_of_none

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
    c.execute("SELECT * FROM country")
    rows = c.fetchall()
    lst = []
    lst2 = []
    print("hello")
    for item in rows[0]:
        lst.append(item)
    for item in rows[1]:
        lst2.append(item)
    c.close()
    return lst,lst2
    
def new_game():
    reset_playercards()
    reset_dealercards()

def check_Aces_P():
    c=db.cursor()
    c.execute("SELECT * FROM playercards")
    rows = c.fetchall()
    lst = []
    for item in rows[0]:
        lst.append(item)
    lst.pop()
    value = get_player_value()
    aces = 0
    aces += lst.count("https://deckofcardsapi.com/static/img/aceDiamonds.png")
    aces += lst.count("https://deckofcardsapi.com/static/img/AC.png")
    aces += lst.count("https://deckofcardsapi.com/static/img/AH.png")
    aces += lst.count("https://deckofcardsapi.com/static/img/AS.png")
    while(value > 21):
        if(aces > 0):
            value -= 10
        if(aces == 0):
            break
        aces-=1

    c.execute("UPDATE playercards SET total_value = ?", (value,))
    c.close()

def check_Aces_D():
    c=db.cursor()
    c.execute("SELECT * FROM dealercards")
    rows = c.fetchall()
    lst = []
    for item in rows[0]:
        lst.append(item)
    lst.pop()
    value = get_player_value()
    aces = 0
    aces += lst.count("https://deckofcardsapi.com/static/img/aceDiamonds.png")
    aces += lst.count("https://deckofcardsapi.com/static/img/AC.png")
    aces += lst.count("https://deckofcardsapi.com/static/img/AH.png")
    aces += lst.count("https://deckofcardsapi.com/static/img/AS.png")
    while(value > 21):
        if(aces > 0):
            value -= 10
        if(aces == 0):
            break
        aces-=1
            
    c.execute("UPDATE dealercards SET total_value = ?", (value,))
    c.close()

def add_Aces_P():
    c=db.cursor()
    c.execute("SELECT * FROM playercards")
    rows = c.fetchall()
    lst = []
    for item in rows[0]:
        lst.append(item)
    lst.pop()
    value = get_player_value()
    aces = 0
    aces += lst.count("https://deckofcardsapi.com/static/img/aceDiamonds.png")
    aces += lst.count("https://deckofcardsapi.com/static/img/AC.png")
    aces += lst.count("https://deckofcardsapi.com/static/img/AH.png")
    aces += lst.count("https://deckofcardsapi.com/static/img/AS.png")
    while(value < 21):
        if(aces > 0):
            value += 10
        if(aces == 0):
            break
        aces-=1

    c.execute("UPDATE playercards SET total_value = ?", (value,))
    c.close()

def add_Aces_D():
    c=db.cursor()
    c.execute("SELECT * FROM dealercards")
    rows = c.fetchall()
    lst = []
    for item in rows[0]:
        lst.append(item)
    lst.pop()
    value = get_player_value()
    aces = 0
    aces += lst.count("https://deckofcardsapi.com/static/img/aceDiamonds.png")
    aces += lst.count("https://deckofcardsapi.com/static/img/AC.png")
    aces += lst.count("https://deckofcardsapi.com/static/img/AH.png")
    aces += lst.count("https://deckofcardsapi.com/static/img/AS.png")
    while(value < 21):
        if(aces > 0):
            value += 10
        if(aces == 0):
            break
        aces-=1
            
    c.execute("UPDATE dealercards SET total_value = ?", (value,))
    c.close()

