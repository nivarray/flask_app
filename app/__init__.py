"""
Initializes the Flask App
Sets up configuration
Registers blueprints
Sets up DB
"""
from flask import Flask
from .routes import main_bp
from .db import get_db, close_db

def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('../config.py')

    # Register blueprints
    app.register_blueprint(main_bp)

    # Teardown DB connection
    @app.teardown_appcontext
    def teardown_db(exception):
        close_db()

    return app