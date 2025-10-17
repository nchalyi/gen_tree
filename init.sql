CREATE TABLE IF NOT EXISTS people (
    id SERIAL PRIMARY KEY,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    mother_id INTEGER NULL,
    father_id INTEGER NULL,
    CONSTRAINT fk_mother FOREIGN KEY (mother_id) REFERENCES people(id) ON DELETE SET NULL,
    CONSTRAINT fk_father FOREIGN KEY (father_id) REFERENCES people(id) ON DELETE SET NULL
);

ALTER TABLE people ADD CONSTRAINT unique_first_name UNIQUE (first_name);