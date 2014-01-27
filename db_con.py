import sqlite3

def connect_db(db = None):
    return sqlite3.connect(db)