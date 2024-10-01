"""
Uses sqlite3 to establish DB connection
Contains functions to get and close the DB connection
"""
import sqlite3
from flask import g
# g is a global request context, stores data temporarily
# for the duration of the request. perfect for db connections.
def get_db():
    # try except handles db connection error
    try:
        if 'db' not in g:
            g.db = sqlite3.connect('instance/app.db')
            g.db.row_factory = sqlite3.Row  # ensures that results are returned as a dictionary-like object, where you can access columns by name.
        return g.db
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return None

#prevents potential resource leaks
def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()

def init_db():
    db = get_db()
    with open('schema.sql', 'r') as f:
        db.executescript(f.read())