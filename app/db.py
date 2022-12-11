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
CREATE TABLE if not exists consoomer(user text, password text, country text);
CREATE TABLE if not exists dabloons(user text, highest real, current real, recent real);
CREATE TABLE if not exists country(country text, GDP int);
""")
c.close()
# c = db.cursor()
# c.execute("select * from consoomer")
# print(c.fetchall())
# c.close()

def user_exists(username):
    c=db.cursor()
    result = c.execute("Select user from consoomer where user = ?", (username))
    try:
        c.fetchone()[0]==username
        c.close()
        return True
    except: #If c.fetchone does not have an entry, then we want to catch the error and return an exception
        c.close()
        return False

def insert(username,password, country):
    c=db.cursor()
    c.execute("Insert into consoomer(?,?,?)", username, password, country)
    c.close()
def check_pass(insert):
        c=db.cursor()
        result = c.execute("Select password from consoomer where user = ?", (username))
        try:
            c.fetchone()[0]== insert
            c.close()
            return True
        except: #If c.fetchone does not have an entry, then we want to catch the error and return an exception
            c.close()
            return False

def update_country(user_new,country_new):
    c=db.cursor()
    db.executescript("""
    UPDATE consoomer
    Set country = ?
    where user=?""", country_new,user_new)
    c.close()
