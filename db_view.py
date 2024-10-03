import sqlite3
"""
Used to quickly view the tables in the database.
Initially used this to check that data was indeed added.
Not super useful since I can just query the DB on the sqlite terminal.
"""
def view_database(db_file):
    # Establish a connection and use cursor to allow database interactions
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    # Get list of tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()

    # loops through all tables, prints them
    print("Tables in DB:")
    for table in tables:
        print(table[0])

    # Fetch and print data from each table
    for table in tables:
        print(f"\nData in {table[0]}:")
        cursor.execute(f"SELECT * FROM {table[0]};")
        rows = cursor.fetchall()
        for row in rows:
            print(row)

    conn.close()

if __name__ == "__main__":
    view_database("instance/app.db")
