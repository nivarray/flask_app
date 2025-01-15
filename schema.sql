/*
SQL tables, sample data is in data.sql for testing purposes
*/
-- Table for Pollen data 
CREATE TABLE IF NOT EXISTS pollens(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    pollen_id INTEGER,
    `name` TEXT NOT NULL,
    `description` TEXT,
    season TEXT,
    other_info TEXT
);

-- Table for Annotation data
CREATE TABLE IF NOT EXISTS annotations(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    pollen_id INTEGER,
    image_id INTEGER,
    Xmid FLOAT,
    Ymid FLOAT,
    width FLOAT,
    height FLOAT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME,
    FOREIGN KEY (pollen_id) REFERENCES pollens (id),
    FOREIGN KEY (image_id) REFERENCES images (id)
);

-- Trigger for column updated_at from annotations table
CREATE TRIGGER IF NOT EXISTS update_annotations_update_at
AFTER UPDATE ON annotations
FOR EACH ROW
BEGIN
    UPDATE annotations
    SET updated_at = CURRENT_TIMESTAMP
    WHERE id = OLD.id;
END;

-- Table for image paths
CREATE TABLE IF NOT EXISTS images(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    pollen_id INTEGER,
    original_image_name TEXT,
    image_path TEXT,
    pollen_name TEXT
);

-- Table for other data
CREATE TABLE IF NOT EXISTS related_data(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    pollen_id INTEGER,
    `data` TEXT,
    FOREIGN KEY (pollen_id) REFERENCES pollens (id)
);
