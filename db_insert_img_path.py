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
    dir_path = 'app/static/img/Gramineae_Poaceae(Grass)'

    dir_path_list = [] 
    for filename in os.listdir(dir_path):
        if filename.endswith('.jpg'):
            full_path = os.path.join(dir_path, filename)
            dir_path_list.append(full_path)

    dir_path_list.sort()

    for i in range(len(dir_path_list)):
        file_name = os.path.basename(dir_path_list[i])
        cursor.execute('INSERT INTO images(original_image_name, image_path) VALUES (?, ?)', (file_name, dir_path_list[i],))

    # print(dir_path_list)

    conn.commit()
    conn.close()

if __name__ == '__main__':
    db_name = "instance/app.db"

    insert_img_path_to_images(db_name)
