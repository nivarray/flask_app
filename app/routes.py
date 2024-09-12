"""
Contains routes and handles HTTP requests
Retrieves data from DB, passes to the templates
"""
from flask import Blueprint, render_template, request, redirect, url_for
from .db import get_db

main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def index():
    db = get_db()
    # Gets the table names from the SQLite database
    table_names = [row[0] for row in db.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall()]  # index.html uses this variable
    return render_template('index.html', table_names=table_names)


@main_bp.route('/query', methods=['POST'])
def query_db():
    selected_table = request.form.get('table_name')
    db = get_db()
    rows = db.execute(f'SELECT * FROM {selected_table}').fetchall()
    return render_template('results.html', rows=rows)

