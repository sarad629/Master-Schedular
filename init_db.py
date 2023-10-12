import sqlite3

"""
Program Initializes database but does not need to run each time app is run
"""

connection = sqlite3.connect('database.db')

with open('schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

connection.commit()
connection.close()