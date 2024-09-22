/*
SQL tables, sample data is in data.sql for testing purposes
*/
-- Table for Pollen data 
CREATE TABLE IF NOT EXISTS pollens(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    `name` TEXT NOT NULL,
    `description` TEXT,
    season TEXT,
    other_info TEXT
);

-- Table for other data
CREATE TABLE IF NOT EXISTS related_data(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    pollen_id TEXT,
    `data` TEXT,
    FOREIGN KEY (pollen_id) REFERENCES pollens (id)
);
