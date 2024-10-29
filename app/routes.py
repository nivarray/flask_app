"""
Contains routes and handles HTTP requests
Retrieves data from DB, passes to the templates
"""
from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from .db import get_db

main_bp = Blueprint('main', __name__)


# Alternative function name: get_pollen_name()
@main_bp.route('/')
def index():
    db = get_db()  # Gets DB connection
    if db is None:
        return jsonify({"error": "Database connection failed"}), 500
    
    # Gets the pollen names from the pollens table
    pollen_names = [row['name'] for row in db.execute("SELECT name FROM pollens").fetchall()]  # index.html uses this variable
    return render_template('index.html', pollen_names=pollen_names)


"""Gets data from the DB and returns it as a json format"""
"""Keep things as small as possible, this function will be used to get the rows with the same name from the pollens table"""
@main_bp.route('/fetch_data', methods=['GET','POST'])
def fetch_data():
    selected_pollen = request.json.get('pollen_name')
    print(f"Selected pollen: {selected_pollen}")  # Log the selected pollen
    db = get_db()
    if db is None:
        return jsonify({"error": "Database connection failed"}), 500
    
    rows = db.execute('SELECT * FROM pollens WHERE name = ?', (selected_pollen,)).fetchall()
    print(f"Fetched rows: {rows}")  # Log fetched rows
    return jsonify([dict(row) for row in rows])  
# row needs to be cast as dict because jsonify can't handle the sqlite3.Row object 
# (which is dictionary-like but not a dict)
# jsonify in python functions is important because the front end of JS expects a JSON object when making fetch requests.


"""Create the next function to join first and second table"""
@main_bp.route('/get_related_data', methods=['GET', 'POST'])
def get_related_data_join():
    selected_pollen = request.json.get('pollen_name')
    db = get_db()
    if db is None:
        return jsonify({"error": "Database connection failed"}), 500
    
    rows = db.execute("SELECT * FROM pollens p JOIN related_data rd ON p.id = rd.pollen_id WHERE p.name= ?;", (selected_pollen,)).fetchall()
    return jsonify([dict(row) for row in rows])  


"""Should return the annotations for selected pollen, JS will have a button"""
@main_bp.route('/get_annotations', methods=['GET', 'POST'])
def get_annotations():
    selected_pollen = request.json.get('pollen_name')
    db = get_db()
    if db is None:
        return jsonify({"error": "Database connection failed"}), 500
    
    rows = db.execute("SELECT a.annotation_text FROM pollens p JOIN annotations a ON p.id=a.pollen_id WHERE p.name= ?;", (selected_pollen,)).fetchall()
    return jsonify([dict(row) for row in rows])