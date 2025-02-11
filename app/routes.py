"""
Contains routes and handles HTTP requests
Retrieves data from DB, passes to the templates
"""
from flask import Blueprint, render_template, request, redirect, url_for, jsonify, current_app, abort
from .db import get_db
import os

# 'main' is the blueprint name, __name__ helps Flask locate resources
main_bp = Blueprint('main', __name__)


# Establishes connection, handles connection errors, reused in other functions
def get_db_connection():
    db = get_db()
    if db is None:
        abort(500, description="Database connection failed")
    return db


"""Gets pollen names from the pollens table, sends to index.html"""
@main_bp.route('/', methods=['GET'])
def get_pollen_name():
    db = get_db_connection() # Establishes DB connection, handles conn errors
    
    # Gets the pollen names from the pollens table
    pollen_names = [row['name'] for row in db.execute("SELECT name FROM pollens").fetchall()]  # index.html uses this variable
    
    return render_template('index.html', pollen_names=pollen_names)


"""Gets data from the DB and returns it as a json format"""
@main_bp.route('/fetch_data', methods=['GET','POST'])
def fetch_data():
    selected_pollen = request.json.get('pollen_name')
    # print(f"Selected pollen: {selected_pollen}")  # Log the selected pollen
    db = get_db_connection() # Establishes DB connection, handles conn errors
    
    rows = db.execute('SELECT * FROM pollens WHERE name = ?', (selected_pollen,)).fetchall()
    print(f"Fetched rows: {[dict(row) for row in rows]}")  # Log fetched rows

    return jsonify([dict(row) for row in rows])  
# row needs to be cast as dict because jsonify can't handle the sqlite3.Row object 
# (which is dictionary-like but not a dict)
# jsonify in python functions is important because the front end of JS expects a JSON object when making fetch requests.


"""Create the next function to join first and second table"""
@main_bp.route('/get_related_data', methods=['GET', 'POST'])
def get_related_data_join():
    selected_pollen = request.json.get('pollen_name')
    db = get_db_connection() # Establishes DB connection, handles conn errors
    
    rows = db.execute("SELECT * FROM pollens p JOIN related_data rd ON p.id = rd.pollen_id WHERE p.name= ?;", (selected_pollen,)).fetchall()

    return jsonify([dict(row) for row in rows])  


"""Should return the annotations for selected pollen, JS will have a button"""
@main_bp.route('/get_annotations', methods=['GET', 'POST'])
def get_annotations():
    selected_pollen = request.json.get('pollen_name')
    db = get_db_connection() # Establishes DB connection, handles conn errors
    
    rows = db.execute("SELECT image_id, Xmid, Ymid, width, height FROM annotations a JOIN pollens p ON a.pollen_id=p.id WHERE p.name=? ORDER BY a.image_id;", (selected_pollen,)).fetchall()
    #rows = db.execute("SELECT a.annotation_text FROM pollens p JOIN annotations a ON p.id=a.pollen_id WHERE p.name= ?;", (selected_pollen,)).fetchall()

    return jsonify([dict(row) for row in rows])


"""Grabs images from the static/img/ directory and sends to the front end"""
@main_bp.route('/fetch_images', methods=['GET', 'POST'])
def fetch_images():
    selected_pollen = request.json.get('pollen_name')

    # Base directory where 'img' folder is located
    img_folder = os.path.join(current_app.static_folder, "img")
    matching_imgs = []

    # Check if the base directory exists
    if not os.path.isdir(img_folder):
        return jsonify({"error": "The base image directory does not exist"}), 400

    # Normalize selected_pollen for comparison
    normalized_selected_pollen = selected_pollen.lower().strip()
    
    # Loop through all subdirectories and their files
    for root, _, files in os.walk(img_folder):
        # Normalize the current directory name
        current_dir_name = os.path.basename(root).lower().strip()

        # Check if the normalized directory name matches the selected pollen
        if current_dir_name == normalized_selected_pollen:
            for filename in sorted(files):
                if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
                    # Construct the file path relative to the 'static' folder
                    relative_path = os.path.relpath(os.path.join(root, filename), current_app.static_folder)
                    file_path = url_for('static', filename=relative_path)
                    matching_imgs.append(file_path)

    # Return the images found or an appropriate message if none found
    if not matching_imgs:
        return jsonify({"message": "No images found for the selected pollen"}), 404
    
    return jsonify(matching_imgs)
