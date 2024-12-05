import sqlite3

def insert_file_values(text_file, db_name):
    """Extracts from a text file and inserts into the desired SQL table"""

    # Establish connection
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    # Read the file
    with open(text_file, 'r') as file:
        for line in file:
            pollen_name = line.rstrip()

            print(f"Inserting: {pollen_name}")
            # insert into table
            try:
                cursor.execute('INSERT INTO pollens (name) VALUES (?)', (pollen_name,))
            except sqlite3.Error as e:
                print(f"Error occured: {e}")
                
    conn.commit()
    conn.close()

if __name__ == '__main__':
    text_file = 'labels.txt'
    db_name = "instance/app.db"

    insert_file_values(text_file, db_name)