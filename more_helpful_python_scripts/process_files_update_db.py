import os
import sqlite3

def process_files_and_update_db(db_name, dir, max_pollen_id=51):

    # Connect to the db
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    
    # Loop from 1-51, thats how many pollen exist in the pollens table
    for pollen_id in range(1, max_pollen_id+1):
        # Query to fetch image data for the current pollen_id
        cursor.execute("""
            SELECT id, original_image_name 
            FROM images 
            WHERE pollen_id=? 
            ORDER BY original_image_name
        """, (pollen_id,))
        
        image_data = cursor.fetchall()
        # Map of {image_name: image_id}
        image_map = {row[1]: row[0] for row in image_data}

        if not image_map:
            print(f"No images found for pollen_id={pollen_id}. Skipping...")
            continue

        # Loop through the files in the directory
        files = sorted(os.listdir(dir)) # Sort by name

        for i, filename in enumerate(files):
            if filename.endswith(".png") or filename.endswith(".jpg"):
                # Find the corresponding annotation file
                image_path = os.path.join(dir, filename)
                annotation_path = os.path.join(dir, files[i + 1]) if i+1 < len(files) else None

                # Skip if no matching annotation file
                if not annotation_path or not annotation_path.endswith(".txt"):
                    print(f"No matching annotation file for {filename}")
                    continue

                # Extract image name without the extension
                image_name = os.path.basename(filename)

                # Skip if image name not found in the database for the current pollen_id
                if image_name not in image_map:
                    print(f"Image {image_name} not found in the database for pollen_id={pollen_id}.")
                    continue

                # Get the image_id for this image
                image_id = image_map[image_name]

                # Read the annotation file and parse its data
                with open(annotation_path, "r") as annotation_file:
                    for line in annotation_file:
                        # Parse teh annotation line
                        data = line.strip().split()
                        if len(data) < 5:
                            print(f"Skipping invalid annotation line in {annotation_path}: {line}")
                            continue

                        annotation_pollen_id, x_mid, y_mid, width, height = data
                        annotation_pollen_id = int(annotation_pollen_id) # Convert pollen_id to integer

                        # Only process annotations matching the current pollen_id
                        if annotation_pollen_id != pollen_id:
                            continue

                        # Update the db
                        update_query = """
                            UPDATE annotations
                            SET image_id = ?
                            WHERE pollen_id = ?
                            AND Xmid = ?
                            AND Ymid = ?
                            AND width = ?
                            AND height = ?
                        """
                        cursor.execute(update_query, (image_id, pollen_id, x_mid, y_mid, width, height))

    # Commit changes and close the connection
    conn.commit()
    conn.close()
    print("Process completed successfully")


if __name__ == '__main__':
    db_name = "instance/app.db"
    dir = "/home/nivar/Documents/pollen_dataset/images"
    process_files_and_update_db(db_name, dir)
