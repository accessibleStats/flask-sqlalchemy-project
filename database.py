"""

Script to generate database instance and create users table 
- run only once, before launching app - no need to run script twice. -

"""


import sqlite3


con = sqlite3.connect('user_database.db')

cur = con.cursor()

cur.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, date DATE, username TEXT, email TEXT, passworda TEXT, passwordb TEXT)")






