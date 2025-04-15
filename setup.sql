-- Create database
CREATE DATABASE IF NOT EXISTS attendance;
USE attendance;

-- Create tables
CREATE TABLE IF NOT EXISTS class (
    class_id INT NOT NULL AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    PRIMARY KEY (class_id)
);

CREATE TABLE IF NOT EXISTS faculty (
    faculty_id INT NOT NULL AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    department VARCHAR(100) NOT NULL,
    faculty_username VARCHAR(50) UNIQUE,
    password VARCHAR(255),
    PRIMARY KEY (faculty_id)
);

CREATE TABLE IF NOT EXISTS subject (
    subject_id INT NOT NULL,
    subject_name VARCHAR(100) NOT NULL,
    faculty_id INT,
    PRIMARY KEY (subject_id),
    FOREIGN KEY (faculty_id) REFERENCES faculty(faculty_id)
);

CREATE TABLE IF NOT EXISTS class_subject (
    class_id INT NOT NULL,
    subject_id INT NOT NULL,
    PRIMARY KEY (class_id, subject_id),
    FOREIGN KEY (class_id) REFERENCES class(class_id),
    FOREIGN KEY (subject_id) REFERENCES subject(subject_id)
);

CREATE TABLE IF NOT EXISTS student (
    stu_id INT NOT NULL AUTO_INCREMENT,
    usn VARCHAR(20) NOT NULL UNIQUE,
    name VARCHAR(100) NOT NULL,
    class_id INT,
    password VARCHAR(255),
    PRIMARY KEY (stu_id),
    FOREIGN KEY (class_id) REFERENCES class(class_id)
);

CREATE TABLE IF NOT EXISTS attendance (
    attendance_id INT NOT NULL AUTO_INCREMENT,
    stu_id INT,
    class_id INT,
    subject_id INT,
    date DATE,
    status ENUM('Present', 'Absent'),
    PRIMARY KEY (attendance_id),
    FOREIGN KEY (stu_id) REFERENCES student(stu_id),
    FOREIGN KEY (class_id) REFERENCES class(class_id),
    FOREIGN KEY (subject_id) REFERENCES subject(subject_id)
);

-- Insert initial data
INSERT INTO class (name) VALUES 
('CSE'),
('ISE'),
('AIML');

INSERT INTO faculty (name, department, faculty_username, password) VALUES
('Prof. Smith', 'Computer Science', 'smith', 'pbkdf2:sha256:600000$tGl7lwaVcdIpmWM5$b701364d2895eda338e1c8c895ab71d8f90fb8a76e00250ccae349d5f3815a24'),
('Prof. Johnson', 'Computer Science', 'johnson', 'pbkdf2:sha256:600000$tGl7lwaVcdIpmWM5$b701364d2895eda338e1c8c895ab71d8f90fb8a76e00250ccae349d5f3815a24'),
('Prof. Williams', 'Mathematics', 'williams', 'pbkdf2:sha256:600000$tGl7lwaVcdIpmWM5$b701364d2895eda338e1c8c895ab71d8f90fb8a76e00250ccae349d5f3815a24'),
('Prof. Brown', 'Environmental Science', 'brown', 'pbkdf2:sha256:600000$tGl7lwaVcdIpmWM5$b701364d2895eda338e1c8c895ab71d8f90fb8a76e00250ccae349d5f3815a24'),
('Prof. Jones', 'Computer Science', 'jones', 'pbkdf2:sha256:600000$tGl7lwaVcdIpmWM5$b701364d2895eda338e1c8c895ab71d8f90fb8a76e00250ccae349d5f3815a24'),
('Prof. Garcia', 'Computer Science', 'garcia', 'pbkdf2:sha256:600000$tGl7lwaVcdIpmWM5$b701364d2895eda338e1c8c895ab71d8f90fb8a76e00250ccae349d5f3815a24');

INSERT INTO subject (subject_id, subject_name, faculty_id) VALUES
(1, 'Database Management System', 1),
(2, 'Computer Networks', 2),
(3, 'Discrete Mathematics Structure', 3),
(4, 'Environmental Science', 4),
(5, 'ATCD', 5),
(6, 'Python Programming', 6);

INSERT INTO class_subject (class_id, subject_id) VALUES
(1, 1), (1, 2), (2, 2), (1, 3), (2, 3), (3, 3),
(1, 4), (3, 4), (2, 5), (3, 5), (2, 6), (3, 6);

-- Note: Add student data as needed
-- Default password for all users is '12345678'