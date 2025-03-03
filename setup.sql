-- Create database
DROP DATABASE attendance;
CREATE DATABASE attendance;
USE attendance;

-- Create tables
CREATE TABLE class (
    class_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(50) NOT NULL,
    department VARCHAR(50) NOT NULL
);

CREATE TABLE faculty (
    faculty_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    faculty_username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    department VARCHAR(50) NOT NULL
);

CREATE TABLE subject (
    subject_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    subject_code VARCHAR(20) UNIQUE NOT NULL
);

CREATE TABLE class_subjects (
    class_id INT,
    subject_id INT,
    faculty_id INT,
    PRIMARY KEY (class_id, subject_id),
    FOREIGN KEY (class_id) REFERENCES class(class_id),
    FOREIGN KEY (subject_id) REFERENCES subject(subject_id),
    FOREIGN KEY (faculty_id) REFERENCES faculty(faculty_id)
);

CREATE TABLE student (
    stu_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    usn VARCHAR(20) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    class_id INT,
    FOREIGN KEY (class_id) REFERENCES class(class_id)
);

CREATE TABLE attendance (
    attendance_id INT PRIMARY KEY AUTO_INCREMENT,
    stu_id INT,
    class_id INT,
    subject_id INT,
    date DATE NOT NULL,
    status ENUM('Present', 'Absent') NOT NULL,
    FOREIGN KEY (stu_id) REFERENCES student(stu_id),
    FOREIGN KEY (class_id) REFERENCES class(class_id),
    FOREIGN KEY (subject_id) REFERENCES subject(subject_id)
);

-- Insert existing data

-- Existing Classes
INSERT INTO class (name, department) VALUES
('ISE-A', 'Information Science'),
('ISE-B', 'Information Science'),
('CSE-A', 'Computer Science'),
('CSE-B', 'Computer Science');

-- Existing Faculty members with their current passwords
INSERT INTO faculty (name, faculty_username, password, department) VALUES
('Dr. Rajesh Kumar', 'rajesh_k', 'pbkdf2:sha256:600000$dK7PVFzg$d8d0463c48c9f97437b8456c7f7fd6bb99d9305fd54f471755ad11ab3d84242c', 'Information Science'),
('Prof. Priya Singh', 'priya_s', 'pbkdf2:sha256:600000$dK7PVFzg$d8d0463c48c9f97437b8456c7f7fd6bb99d9305fd54f471755ad11ab3d84242c', 'Information Science'),
('Dr. Amit Sharma', 'amit_s', 'pbkdf2:sha256:600000$dK7PVFzg$d8d0463c48c9f97437b8456c7f7fd6bb99d9305fd54f471755ad11ab3d84242c', 'Computer Science');

-- Existing Subjects
INSERT INTO subject (name, subject_code) VALUES
('ATCD', 'CS201'),
('Computer Networks', 'CS202'),
('Discrete Mathematics Structure', 'CS203'),
('Python Programming', 'CS204');

-- Existing Class-Subject mapping
INSERT INTO class_subjects (class_id, subject_id, faculty_id) VALUES
(1, 1, 1), -- ISE-A: ATCD by Dr. Rajesh
(1, 2, 2), -- ISE-A: Computer Networks by Prof. Priya
(1, 3, 3), -- ISE-A: Discrete Mathematics by Dr. Amit
(1, 4, 1); -- ISE-A: Python Programming by Dr. Rajesh

-- Existing students with their current passwords
INSERT INTO student (name, usn, password, class_id) VALUES
('John Doe', '1SI20IS001', 'pbkdf2:sha256:600000$dK7PVFzg$d8d0463c48c9f97437b8456c7f7fd6bb99d9305fd54f471755ad11ab3d84242c', 1),
('Jane Smith', '1SI20IS002', 'pbkdf2:sha256:600000$dK7PVFzg$d8d0463c48c9f97437b8456c7f7fd6bb99d9305fd54f471755ad11ab3d84242c', 1),
('Bob Wilson', '1SI20IS003', 'pbkdf2:sha256:600000$dK7PVFzg$d8d0463c48c9f97437b8456c7f7fd6bb99d9305fd54f471755ad11ab3d84242c', 1);

-- Sample queries for reference:

-- Get all students in ISE-A class
SELECT s.name, s.usn 
FROM student s 
JOIN class c ON s.class_id = c.class_id 
WHERE c.name = 'ISE-A';

-- Get all subjects for ISE-A class
SELECT s.name, s.subject_code, f.name as faculty_name
FROM subject s
JOIN class_subjects cs ON s.subject_id = cs.subject_id
JOIN faculty f ON cs.faculty_id = f.faculty_id
JOIN class c ON cs.class_id = c.class_id
WHERE c.name = 'ISE-A';

-- Get attendance for a specific student
SELECT s.name, sub.name as subject, a.date, a.status
FROM attendance a
JOIN student s ON a.stu_id = s.stu_id
JOIN subject sub ON a.subject_id = sub.subject_id
WHERE s.usn = '1SI20IS001'
ORDER BY a.date; 