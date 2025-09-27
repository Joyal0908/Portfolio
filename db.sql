CREATE DATABASE portfolio_db;
USE portfolio_db;


CREATE TABLE skills (
    id INT AUTO_INCREMENT PRIMARY KEY,
    category VARCHAR(100) NOT NULL,
    name VARCHAR(100) NOT NULL,
    icon_class VARCHAR(100) DEFAULT NULL,
    description TEXT,
    proficiency_level VARCHAR(50) DEFAULT NULL,
    proficiency_percent INT DEFAULT 0
);

CREATE TABLE contact_messages (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255),
    email VARCHAR(255),
    message TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE project_status (
    id INT AUTO_INCREMENT PRIMARY KEY,
    project_no INT NOT NULL,
    project_title VARCHAR(255) NOT NULL,
    status ENUM('completed', 'ongoing') NOT NULL DEFAULT 'ongoing',
    client_name VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    description TEXT,
	link VARCHAR(255)
);

