"""
Config settings
"""

import os

SECRET_KEY = 'your_secret_key'  # will change this to an actual key later
DATABASE = os.path.join(os.getcwd(), 'instance', 'app.db')