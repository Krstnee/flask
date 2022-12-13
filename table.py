import sqlite3

with sqlite3.connect('users.db') as con:
    cur = con.cursor()
    cur.execute('drop table users')
    cur.execute('create table users (username text, password text, date text)')