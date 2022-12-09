"""
Practical Jokers
Softdev P01
2022-12-07
time spent: 3 hours
"""
import sqlite3
DB_FILE="back.db"
db=sqlite3.connect(DB_FILE, check_same_thread=False)
c=db.cursor()

db.execute("CREATE TABLE if not exists consoomer(user text, password text, country text)")

db.execute("CREATE TABLE if not exists dabloons(user text, highest real, current real, recent real)")

db.execute("CREATE TABLE if not exists country(country text, GDP int)")

db.execute("Insert into country values('USA',0)")

db.execute("Insert into consoomer values(?,?,?)", "Ameer", "Alnasser", "USA")

db.execute()
def user_exists(username):
    c=db.cursor()
    result=c.execute("Select user from consoomer where username = ?", username)
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
 