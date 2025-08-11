CREATE DATABASE IF NOT EXISTS school;
USE school;

CREATE TABLE rooms (
    id INT PRIMARY KEY,
    name VARCHAR(50) NOT NULL
);

CREATE TABLE students (
    id INT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    birthday DATE NOT NULL,
    sex ENUM('M', 'F') NOT NULL,
    room_id INT NOT NULL,
    FOREIGN KEY (room_id) REFERENCES rooms(id)
        ON UPDATE CASCADE
);
