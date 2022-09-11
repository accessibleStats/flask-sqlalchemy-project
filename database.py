"""

Script to generate database instance - run only once, before launching app

"""


import sqlite3


con = sqlite3.connect('user_database.db')

cur = con.cursor()

cur.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, date DATE, username TEXT, email TEXT, passworda TEXT, passwordb TEXT)")






