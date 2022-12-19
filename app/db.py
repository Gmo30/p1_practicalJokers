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
CREATE TABLE if not exists dabloons(user text, country text, highest real, current real, recent real);
CREATE TABLE if not exists country(country text, GDP int);
CREATE TABLE if not exists dealercards(cardname text, cardname1 text, cardname2 text,cardname3 text, 
    cardname4 text, cardname5 text, cardname6 text, cardname7 text, cardname8 text,
    cardname9 text, cardname10 text, cardname11 text,  total_value int);
CREATE TABLE if not exists playercards(cardname text, cardname1 text, cardname2 text,cardname3 text, 
    cardname4 text, cardname5 text, cardname6 text, cardname7 text, cardname8 text,
    cardname9 text, cardname10 text, cardname11 text,  total_value int);
Insert into dealercard values('None','None','None','None','None','None','None','None','None','None','None','None',0);
Insert into playercard values('None','None','None','None','None','None','None','None','None','None','None','None',0);
Insert into consoomer values(?,?,?,?), ('aa', 'password', 'USA', '1000');
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
    db.execute("UPDATE consoomer Set country = ? where user=?", country_new,user_new)
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

def add_player_card(card):
    c=db.cursor()
    c.execute()
    c.close()
def add_dealer(card):
    c=db.cursor()
    c.execute()
    c.close()

def reset_cards():
    c=db.cursor()
    c.executescript("""
    CREATE TABLE 
    dealercards(cardname text, cardname1 text, cardname2 text,cardname3 text, 
    cardname4 text, cardname5 text, cardname6 text, cardname7 text, cardname8 text,
    cardname9 text, cardname10 text, cardname11 text,  total_value int);
    CREATE TABLE
     playercards(cardname text, cardname1 text, cardname2 text,cardname3 text, 
    cardname4 text, cardname5 text, cardname6 text, cardname7 text, cardname8 text,
    cardname9 text, cardname10 text, cardname11 text,  total_value int);
    Insert into dealercard values('None','None','None','None','None','None','None','None','None','None','None','None',0);
    Insert into playercard values('None','None','None','None','None','None','None','None','None','None','None','None',0);
    """)