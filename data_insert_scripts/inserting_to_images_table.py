import sqlite3
import os

def inserting_to_images_table(db_name):
    """
    Grabs full image paths and inserts into images table.
    Each record includes the file name and its full path.
    """

    # Establish connection
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    # Base directory
    dir_path = 'app/static/img'

    # Traverse through the directories and subdirectories
    for root, dirs, files in os.walk(dir_path):
        print(f"Root: {root}, Dirs: {dirs}, Files: {files}")
        subfolder_name = os.path.basename(root)  # This gets the last part of the path (subfolder)

        # Traverse through files in each subfolder
        for file in files:
            if file.lower().endswith(('.jpg', '.jpeg','.png')):
                # Check if the file is an image (you can add more conditions as needed)
                full_path = os.path.join(root, file)
                file_name = file

                # Insert the image details into the database
                cursor.execute('INSERT INTO images(original_image_name, image_path, pollen_name) VALUES(?, ?, ?)', (file_name, full_path, subfolder_name))

    conn.commit()
    conn.close()

if __name__ == '__main__':
    db_name = "instance/app.db"
    inserting_to_images_table(db_name)
