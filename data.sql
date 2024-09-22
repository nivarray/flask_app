-- Example data
DELETE FROM pollens; -- Remove all existing rows
DELETE FROM sqlite_sequence WHERE name='pollens'; -- Reset the auto-increment counter
INSERT INTO pollens (name, description, season, other_info) VALUES 
('birch', 'Commonly produced by birch trees, this pollen is a significant allergen in early spring.', 'Spring', 'Additional Info1'),
('oak', 'Oak trees release large amounts of pollen in spring, contributing to allergies during this season.', 'Spring', 'Additional Info2'),
('grass', 'Widely found in fields and gardens, causing allergies in late spring and summer.', 'Spring', 'Additional Info3'),
('ragweed', 'Notorious for causing fall allergies, with its pollen released in late summer', 'Summer', 'Additional Info1'),
('knotweed', 'Produces pollen that can cause allergies in late summer.', 'Summer', 'Additional Info2'),
('cedar', 'Can trigger seasonal allergies in winter and early spring, particularly in areas with cedar trees.', 'Winter', 'Additional Info1'),
('pine', 'Release pollen in the spring, which can be a common allergen for many people.', 'Spring', 'Additional Info2');