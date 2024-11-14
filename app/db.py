"""
Uses sqlite3 to establish DB connection
Contains functions to get and close the DB connection
"""
import sqlite3
from flask import g, current_app

# g is a global request context, stores data temporarily
# for the duration of the request. perfect for db connections.
def get_db():
    # Try except handles db connection error
    try:
        if 'db' not in g:
            g.db = sqlite3.connect('instance/app.db')
            # Ensures that results are returned as a dictionary-like object, where you can access columns by name.
            # column names become accessible as keys
            g.db.row_factory = sqlite3.Row  
        return g.db
    except sqlite3.Error as e:
        current_app.logger.error(f"Database error: {e}")
        raise
        # print(f"Database error: {e}")
        # return None


# Prevents potential resource leaks
def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()


# Connects to DB and runs commands from schema
def init_db():
    db = get_db()
    with open('schema.sql', 'r') as f:
        db.executescript(f.read())