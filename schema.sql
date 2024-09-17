/*
SQL tables, sample data for testing purposes
*/
-- Table for Pollen data 
CREATE TABLE IF NOT EXISTS pollens(
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    `name` TEXT NOT NULL,
    `description` TEXT,
    season TEXT,
    other_info TEXT
);

-- Table for other data
CREATE TABLE IF NOT EXISTS related_data(
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    pollen_id TEXT,
    `data` TEXT,
    FOREIGN KEY (pollen_id) REFERENCES pollens (id)
);


-- Example data
INSERT INTO pollens (name, description, season, other_info) VALUES 
('Pollen1', 'Description of Pollen1', 'Spring', 'Additional Info1'),
('Pollen2', 'Description of Pollen2', 'Summer', 'Additional Info2'),
('Pollen3', 'Description of Pollen3', 'Fall', 'Additional Info3');