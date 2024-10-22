"""
Main entry point to run the Flask App
"""
from app import create_app

app = create_app()

# Runs the application in Debug
# Debug provides detailed error, and auto-reloads on code changes
if __name__ == '__main__':
    app.run(debug=True)