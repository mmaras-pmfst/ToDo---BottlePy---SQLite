import sqlite3 as lite
import sys

con=lite.connect('data\\todo.db')

print ("Creating database/tables...")
with con:
    cur =con.cursor()
    #DROP TABLE
    cur.execute("DROP TABLE IF EXISTS todo")
    
    #CREATE TABLE todo
    cur.execute("CREATE TABLE IF NOT EXISTS todo (id INTEGER PRIMARY KEY AUTOINCREMENT, user_id TEXT, title TEXT, desc TEXT, datetime TEXT, datetime_complete TEXT,timetable TEXT)")
    
    #CREATE TABLE users
    cur.execute("CREATE TABLE IF NOT EXISTS user (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT, password TEXT, email TEXT)")
con.close()
print ("Database/tables created.")
