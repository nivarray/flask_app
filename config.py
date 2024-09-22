"""
Config settings
"""

import os

SECRET_KEY = 'secret_key'  # will change this to an actual key later
DATABASE = os.path.join(os.getcwd(), 'instance', 'app.db')