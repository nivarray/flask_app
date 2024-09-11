"""
Config settings
"""

import os

SECRET_KEY = 'your_secret_key'
DATABASE = os.path.join(os.getcwd(), 'instance', 'app.db')