-- Create the users table
CREATE TABLE users
(
    ID BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    name_encr BLOB NULL,
    hashedPassword TEXT NULL,

    PRIMARY KEY (ID)
) ENGINE = InnoDB;

-- Create the days table
CREATE TABLE days
(
    ID BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    year INT NOT NULL,
    month INT NOT NULL,
    day INT NOT NULL,

    PRIMARY KEY (ID)
) ENGINE = InnoDB;

-- Create the meal_types table
CREATE TABLE meal_types
(
    ID BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    name TEXT NOT NULL,

    PRIMARY KEY (ID)
) ENGINE = InnoDB;

-- Insert the predefined meal types (breakfast, lunch, dinner, snacks)
INSERT INTO meal_types (name) VALUES
('breakfast'),
('lunch'),
('dinner'),
('snacks');

-- Create the meals table
CREATE TABLE meals
(
    ID BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    fat_level INT NOT NULL,  -- 0: Low, 1: Medium, 2: High
    sugar_level INT NOT NULL, -- 0: Low, 1: Medium, 2: High

    PRIMARY KEY (ID)
) ENGINE = InnoDB;

-- Create the day_meals table with composite primary key
CREATE TABLE day_meals
(
    fk_user_id BIGINT UNSIGNED NOT NULL,    -- Foreign key to users
    fk_day_id BIGINT UNSIGNED NOT NULL,     -- Foreign key to days
    fk_meal_type_id BIGINT UNSIGNED NOT NULL, -- Foreign key to meal_types
    fk_meal_id BIGINT UNSIGNED NOT NULL,    -- Foreign key to meals

    PRIMARY KEY (fk_user_id, fk_day_id, fk_meal_type_id), -- Composite primary key

    CONSTRAINT fk_user FOREIGN KEY (fk_user_id) REFERENCES users(ID) ON DELETE CASCADE,
    CONSTRAINT fk_day FOREIGN KEY (fk_day_id) REFERENCES days(ID) ON DELETE CASCADE,
    CONSTRAINT fk_meal_type FOREIGN KEY (fk_meal_type_id) REFERENCES meal_types(ID) ON DELETE CASCADE,
    CONSTRAINT fk_meal FOREIGN KEY (fk_meal_id) REFERENCES meals(ID) ON DELETE CASCADE
) ENGINE = InnoDB;
