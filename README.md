# Pollen Image + Annotation Viewer

## Description

The Pollen Annotation Viewer is a Flask web application that allows users to sift through pollen names and retrieve microscopic images of pollen along with all related annotations. This application is designed for efficient data retrieval and user-friendly interaction. 

**READ COMMENTS**

## Features

- Dropdown menu for selecting pollen names
- Display of corresponding pollen images
- Presentation of annotations associated with selected pollen
- Option to download images and annotations as a ZIP file

## Technologies Used

- **Backend**: Flask
- **Database**: SQLite (For now)
- **Frontend**: HTML, CSS, JavaScript (Bootstrap, jinja2, JSZip, FileSaver)
- **Image Storage**: Local directory on PC

## Installation

1. Clone this repository:
    ```bash
    git clone https://github.com/nivarray/flask_app.git

2. Create a virtual environment and activate it:
    python -m venv venv
    source venv/bin/activate   # For Windows use `venv\Scripts\activate`

3. Install the required dependencies:
    pip install -r requirements.txt

4. Set up the database:
    Depending on the situation, you may choose to use something like SQLite. Be sure to update apt before installing sqlite (sudo apt update).
    ```bash
    sudo apt install sqlite3

    Maybe you already have a RDBMS to use for the purposes of this project.

5. Run the Flask application:
    ```bash
    flask run