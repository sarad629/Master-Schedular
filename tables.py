import sqlite3 

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

def initialize_tables():
    conn = get_db_connection()
    conn.execute("DROP TABLE IF EXISTS posts")
    conn.execute("""
                 CREATE TABLE posts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    firstname TEXT NOT NULL,
                    lastname TEXT NOT NULL
                );
                 """)
    
    conn.execute("""CREATE TABLE IF NOT EXISTS classes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
        class TEXT NOT NULL,
        period1 INTEGER NOT NULL,
        period2 INTEGER NOT NULL,
        period3 INTEGER NOT NULL,
        period4 INTEGER NOT NULL,
        period5 INTEGER NOT NULL,
        period6 INTEGER NOT NULL,
        period7 INTEGER NOT NULL,
        period8 INTEGER NOT NULL
    );""")

    conn.execute("""CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRiMARY KEY AUTOINCREMENT,
        username TINYTEXT NOT NULL,
        password TINYTEXT NOT NULL,
        hierarchy TINYTEXT NOT NULL,
        school TINYTEXT NOT NULL
    );""")
    
    conn.commit()
    conn.close()