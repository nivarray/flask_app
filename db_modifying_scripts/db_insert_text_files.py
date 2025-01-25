import sqlite3
import os

def insert_into_annotations_table(db_name):
    """Extracts text files from a directory and inserts into the desired SQL table"""

    # Establish connection
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    #Create a for loop to go through each annotation_text_files sub folder to then be used in the dir_path variable below

    #provide directory path
    dir_path = 'app/static/annotation_text_files/'

    # open directory, read each file one by one

    for filename in sorted(os.listdir(dir_path)):
        if filename.endswith(".txt"):
            full_path = os.path.join(dir_path, filename)

            with open(full_path, 'r') as file:
                for line in file:
                    value = line.split(" ")
                    pollen_id = value[0]
                    Xmid = value[1]
                    Ymid = value[2]
                    width = value[3]
                    height = value[4]
                    cursor.execute("INSERT INTO annotations(pollen_id, Xmid, Ymid, width, height) VALUES(?, ?, ?, ?, ?)", (pollen_id, Xmid, Ymid, width, height,))

    conn.commit()
    conn.close()

if __name__ == '__main__':
    db_name = "instance/app.db"

    insert_into_annotations_table(db_name)