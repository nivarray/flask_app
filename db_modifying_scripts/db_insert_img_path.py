import sqlite3
import os

def insert_img_path_to_images(db_name):
    """Grabs full image paths and inserts into images table"""
    """
    INSERT INTO images (original_image_name, image_path) 
    VALUES()
    """

    # Establish connection
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    # Directoty path
    dir_path = 'app/static/annotation_and_img/'

    # Get and sort relevant files
    image_files = sorted(
        [os.path.join(dir_path, f) for f in os.listdir(dir_path) if f.startswith("grass-Poa") and f.endswith('.jpg')]
    )
    print(len(image_files))
    for full_path in image_files:
        file_name = os.path.basename(full_path)
        #cursor.execute('INSERT INTO images(original_image_name, image_path, pollen_id) VALUES (?, ?, ?)', (file_name, dir_path_list[i], 33))
        # Insert only if original_image_name does not exist in the table
        cursor.execute('''
            INSERT INTO images(original_image_name, image_path, pollen_name, pollen_id) 
            SELECT ?, ?, ?, ? WHERE NOT EXISTS (
                SELECT 1 FROM images WHERE original_image_name = ?
            )
        ''', (file_name, full_path, "Gramineae Poaceae (Grass)", 33, file_name))

    conn.commit()
    conn.close()

if __name__ == '__main__':
    db_name = "instance/app.db"

    insert_img_path_to_images(db_name)
