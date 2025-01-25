import sqlite3

def update_table(db_name):
    # Establish connection
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    # The subquery after WHERE EXISTS ensures that the update only happens 
    # for rows in the images table where a matching pollen_name exists in the pollens table
    update_query = """
    UPDATE images 
    SET pollen_id = (
        SELECT id 
        FROM pollens 
        WHERE pollens.name = images.pollen_name
    )
    WHERE EXISTS (
        SELECT 1
        FROM pollens
        WHERE pollens.name = images.pollen_name 
        );"""
    # Runs the updates based on table:pollens column:id and table:image column:pollen_name
    cursor.execute(update_query)

    # Commit changes to the db
    conn.commit()
    conn.close()

if __name__ == '__main__':
    db_name = "instance/app.db"
    update_table(db_name)