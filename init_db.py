import sqlite3
from tables import initialize_tables

"""
Program Initializes database but does not need to run each time app is run
"""
def init_db():
    connection = sqlite3.connect('database.db')
    cur = connection.cursor()
    initialize_tables()
    connection.commit()
    connection.close()