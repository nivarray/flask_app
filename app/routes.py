"""
Contains routes and handles HTTP requests
Retrieves data from DB, passes to the templates
###################this has been reviewed by me, go on to index.html!##############
"""
from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from .db import get_db

main_bp = Blueprint('main', __name__)

# ALREADY REVIEWED
@main_bp.route('/')
def index():
    db = get_db()  # gets DB connection
    # Gets the pollen names from the database
    pollen_names = [row['names'] for row in db.execute("SELECT name FROM pollens").fetchall()]  # index.html uses this variable
    return render_template('index.html', pollen_names=pollen_names)


@main_bp.route('/query', methods=['POST'])
def query_db():
    selected_pollen = request.form.get('pollen_name')  # gets user chosen pollen
    db = get_db()  # gets DB connection
    rows = db.execute('SELECT * FROM pollens WHERE name = ?', (selected_pollen,)).fetchall()
    # rows = db.execute(f'SELECT * FROM {selected_pollen}').fetchall()
    return render_template('results.html', rows=rows)


@main_bp.route('/fetch_data', methods=['POST'])
def fetch_data():
    selected_pollen = request.json.get('pollen_name')
    db = get_db()
    rows = db.execute('SELECT * FROM pollens WHERE name = ?', (selected_pollen,)).fetchall()
    return jsonify([dict(row) for row in rows])  
# row needs to be cast as dict because jsonify can't handle the sqlite3.Row object 
# (which is dictionary-like but not a dict)