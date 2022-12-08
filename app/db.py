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

db.execute("CREATE TABLE if not exists consoomer(username text, password text, country text)")

db.execute("CREATE TABLE if not exists dabloons(username text, highest real, current real, recent real)")

db.execute("CREATE TABLE if not exists country(country text, GDP real)")

db.execute("Insert into country(USA,0)")
