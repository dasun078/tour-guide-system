SET FOREIGN_KEY_CHECKS = 0;

DROP DATABASE IF EXISTS tour_guide_system;
CREATE DATABASE IF NOT EXISTS tour_guide_system;
USE tour_guide_system;

-- Existing tables
CREATE TABLE destinations (
  id INT NOT NULL AUTO_INCREMENT,
  name VARCHAR(100) NOT NULL,
  description TEXT NULL,
  image_url VARCHAR(255) NULL,
  location_coordinates VARCHAR(100) NULL,
  PRIMARY KEY (id)
) ENGINE = InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE activities (
  id INT NOT NULL AUTO_INCREMENT,
  name VARCHAR(100) NOT NULL,
  description TEXT NULL,
  price DECIMAL(10,2) NULL,
  destination_id INT NULL,
  PRIMARY KEY (id),
  INDEX destination_id (destination_id),
  CONSTRAINT activities_ibfk_1
    FOREIGN KEY (destination_id)
    REFERENCES destinations (id)
    ON DELETE SET NULL
) ENGINE = InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE users (
  id INT NOT NULL AUTO_INCREMENT,
  name VARCHAR(100) NOT NULL,
  email VARCHAR(100) NOT NULL,
  password VARCHAR(255) NOT NULL,
  phone VARCHAR(15) NULL,
  is_admin BOOLEAN DEFAULT FALSE,
  created_at TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  UNIQUE INDEX email (email)
) ENGINE = InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE admins (
  id INT NOT NULL AUTO_INCREMENT,
  username VARCHAR(100) NOT NULL,
  password VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  UNIQUE INDEX username (username)
) ENGINE = InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE trips (
  id INT NOT NULL AUTO_INCREMENT,
  user_id INT NOT NULL,
  destination VARCHAR(100) NOT NULL,
  activities TEXT NULL,
  budget DECIMAL(10,2) NULL,
  trip_date DATE NULL,
  created_at TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP,
  coordinates VARCHAR(100) NULL,
  PRIMARY KEY (id),
  INDEX user_id (user_id),
  CONSTRAINT trips_ibfk_1
    FOREIGN KEY (user_id)
    REFERENCES users (id)
    ON DELETE CASCADE
) ENGINE = InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE bookings (
  id INT NOT NULL AUTO_INCREMENT,
  user_id INT NOT NULL,
  trip_id INT NOT NULL,
  activity_id INT NULL,
  booking_date TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  INDEX user_id (user_id),
  INDEX trip_id (trip_id),
  INDEX activity_id (activity_id),
  CONSTRAINT bookings_ibfk_1
    FOREIGN KEY (user_id)
    REFERENCES users (id)
    ON DELETE CASCADE,
  CONSTRAINT bookings_ibfk_2
    FOREIGN KEY (trip_id)
    REFERENCES trips (id)
    ON DELETE CASCADE,
  CONSTRAINT bookings_ibfk_3
    FOREIGN KEY (activity_id)
    REFERENCES activities (id)
    ON DELETE SET NULL
) ENGINE = InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE news (
  id INT NOT NULL AUTO_INCREMENT,
  title VARCHAR(200) NOT NULL,
  content TEXT NULL,
  image_url VARCHAR(255) NULL,
  published_date TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (id)
) ENGINE = InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE reviews (
  id INT NOT NULL AUTO_INCREMENT,
  user_id INT NOT NULL,
  destination_id INT NULL,
  activity_id INT NULL,
  rating INT NULL,
  comment TEXT NULL,
  created_at TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  INDEX user_id (user_id),
  INDEX destination_id (destination_id),
  INDEX activity_id (activity_id),
  CONSTRAINT reviews_ibfk_1
    FOREIGN KEY (user_id)
    REFERENCES users (id)
    ON DELETE CASCADE,
  CONSTRAINT reviews_ibfk_2
    FOREIGN KEY (destination_id)
    REFERENCES destinations (id)
    ON DELETE SET NULL,
  CONSTRAINT reviews_ibfk_3
    FOREIGN KEY (activity_id)
    REFERENCES activities (id)
    ON DELETE SET NULL
) ENGINE = InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- New tables
CREATE TABLE payments (
  id INT NOT NULL AUTO_INCREMENT,
  user_id INT NOT NULL,
  trip_id INT NOT NULL,
  amount DECIMAL(10,2) NOT NULL,
  payment_date TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP,
  payment_status ENUM('Pending', 'Completed', 'Failed') NOT NULL DEFAULT 'Pending',
  PRIMARY KEY (id),
  INDEX user_id (user_id),
  INDEX trip_id (trip_id),
  CONSTRAINT payments_ibfk_1
    FOREIGN KEY (user_id)
    REFERENCES users (id)
    ON DELETE CASCADE,
  CONSTRAINT payments_ibfk_2
    FOREIGN KEY (trip_id)
    REFERENCES trips (id)
    ON DELETE CASCADE
) ENGINE = InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE notifications (
  id INT NOT NULL AUTO_INCREMENT,
  user_id INT NOT NULL,
  message TEXT NOT NULL,
  is_read BOOLEAN DEFAULT FALSE,
  created_at TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  INDEX user_id (user_id),
  CONSTRAINT notifications_ibfk_1
    FOREIGN KEY (user_id)
    REFERENCES users (id)
    ON DELETE CASCADE
) ENGINE = InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- New views
CREATE VIEW user_trips_view AS
SELECT 
  u.id AS user_id, 
  u.name AS user_name, 
  t.id AS trip_id, 
  t.destination, 
  t.trip_date, 
  t.budget, 
  t.coordinates
FROM users u
JOIN trips t ON u.id = t.user_id;

CREATE VIEW activity_reviews_view AS
SELECT 
  a.id AS activity_id, 
  a.name AS activity_name, 
  r.rating, 
  r.comment 
FROM activities a
LEFT JOIN reviews r ON a.id = r.activity_id;

SET FOREIGN_KEY_CHECKS = 1;
