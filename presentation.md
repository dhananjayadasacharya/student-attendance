# Student Attendance Management System
### A Python-based GUI Application

---

# System Overview
- User Management System for Student Attendance
- Built with Python, Tkinter, and MySQL
- Secure Password Management
- Class and Subject Integration

---

# Key Features

### 1. Faculty Management
- Add New Faculty Members
- Department-wise Organization
- Secure Login Credentials
- Password Reset Capability

### 2. Student Management
- Add New Students with USN
- Class Assignment
- Secure Password System
- Automatic Class Integration

### 3. Security Features
- Password Hashing (pbkdf2:sha256)
- Input Validation
- Error Handling
- Database Security

---

# Database Structure

### Core Tables
1. `faculty`
   - Faculty information and credentials
   - Department assignment
   - Unique username system

2. `student`
   - Student details with USN
   - Class assignment
   - Password management

3. `class` & `subject`
   - Class organization
   - Subject management
   - Faculty-subject mapping

---

# User Interface

### 1. Add Faculty Tab
- Name Entry
- Username Creation
- Password Setting
- Department Selection

### 2. Add Student Tab
- Name Entry
- USN Assignment
- Password Setting
- Class Selection Dropdown

### 3. Reset Password Tab
- User Type Selection
- Username/USN Entry
- New Password Setting

---

# Technical Implementation

### Backend
- MySQL Database
- Foreign Key Relationships
- Data Integrity Constraints

### Security
- Werkzeug Security
- Password Hashing
- Input Validation

### Frontend
- Tkinter GUI
- User-friendly Forms
- Dropdown Menus
- Error Messages

---

# Current Setup

### Classes
- ISE-A, ISE-B (Information Science)
- CSE-A, CSE-B (Computer Science)

### Subjects
- ATCD (CS201)
- Computer Networks (CS202)
- Discrete Mathematics Structure (CS203)
- Python Programming (CS204)

---

# Database Queries

### Sample Operations
```sql
-- Get students in ISE-A
SELECT s.name, s.usn 
FROM student s 
JOIN class c ON s.class_id = c.class_id 
WHERE c.name = 'ISE-A';

-- Get subjects for ISE-A
SELECT s.name, s.subject_code, f.name as faculty_name
FROM subject s
JOIN class_subjects cs ON s.subject_id = cs.subject_id
JOIN faculty f ON cs.faculty_id = f.faculty_id
WHERE cs.class_id = 1;
```

---

# Error Handling

### Types of Errors Handled
- Database Connection Issues
- Duplicate Entries
- Invalid Input Data
- Missing Required Fields
- Foreign Key Violations

### User Feedback
- Clear Error Messages
- Success Notifications
- Input Validation Alerts

---

# Future Enhancements

1. Attendance Taking Interface
2. Report Generation
   - Daily Reports
   - Monthly Statistics
   - Subject-wise Analysis

3. Additional Features
   - Email Notifications
   - Mobile App Integration
   - Dashboard Analytics

---

# Thank You

### Contact Information
- Project Repository: [GitHub Link]
- Documentation: README.md
- Support: [Your Contact]

### Questions? 