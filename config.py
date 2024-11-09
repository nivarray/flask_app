"""
Config settings
"""

import os
# Load env variables from .env file
from dotenv import load_dotenv

load_dotenv() # Load var from .env into the environment
SECRET_KEY = os.environ.get('SECRET_KEY')  # Use a secure default for local development only
DATABASE = os.path.join(os.getcwd(), 'instance', 'app.db')