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
CREATE TABLE if not exists cards(deck_id text, total_value int);
Insert into consoomer values(?,?,?,?)", ('aa', 'password', 'USA', '1000');
""")
c.close()
#c = db.cursor()
#c.execute("select * from consoomer")
#print(c.fetchall())
#c.close()

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
    db.executescript("""
    UPDATE consoomer
    Set country = ?
    where user=?""", country_new,user_new)
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