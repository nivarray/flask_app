"""
Uses sqlite3 to establish DB connection
Contains functions to get and close the DB connection
"""
import sqlite3
from flask import g
############## ASK CHATGPT WHAT g IS AGAIN!!!!!!!!
def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect('instance/app.db')
        g.db.row_factory = sqlite3.Row
    return g.db

def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()