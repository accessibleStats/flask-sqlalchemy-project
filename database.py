"""

Script to generate database instance and create users table 
- run only once, before launching app - no need to run script twice. -

"""

# sqlite3 is a built-in module, no need to install
import sqlite3

# connect command creates and connects to database
con = sqlite3.connect('user_database.db')

# cursor object allows us to execute SQL commands
cur = con.cursor()

# execute SQL command to create table
cur.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, date DATE, username TEXT, email TEXT, passworda TEXT, passwordb TEXT, password TEXT)")