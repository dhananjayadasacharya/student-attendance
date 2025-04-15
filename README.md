# Student-Faculty Attendance Management System

A web-based attendance management system built with Flask and MySQL, featuring separate interfaces for students and faculty members.

## Features

- **Login System**
  - Separate login for students and faculty
  - Session management
  - Secure authentication

- **Faculty Features**
  - Take attendance for classes
  - Edit previous attendance records
  - View attendance reports (class-wise and individual)
  - Interactive dashboard

- **Student Features**
  - View attendance percentage for all subjects
  - Progress bar with color indicators
  - Detailed attendance history

## Prerequisites

- Python 3.8 or higher
- MySQL Server
- MySQL Workbench (for database setup)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/dhananjayadasacharya/student-attendance.git
cd student-attendance
```

2. Create a virtual environment and activate it:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install the required packages:
```bash
pip install -r requirements.txt
```

4. Set up the MySQL database:
   - Open MySQL Workbench
   - Execute the SQL commands provided in the database setup section
   - Update the MySQL configuration in `app.py` with your credentials

5. Create a `.env` file in the project root:
```
MYSQL_HOST=localhost
MYSQL_USER=your_username
MYSQL_PASSWORD=your_password
MYSQL_DB=attendance
```

## Database Setup

The database setup SQL commands are already executed. The database includes:
- Tables for students, faculty, subjects, classes, and attendance
- Sample data for testing
- Foreign key relationships for data integrity

## Running the Application

1. Activate the virtual environment if not already activated:
```bash
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Run the Flask application:
```bash
python app.py
```

3. Access the application at `http://localhost:5000`

## Usage

### Faculty Login
- Use faculty name as username
- Access the dashboard to manage attendance
- Take attendance for classes
- Edit previous attendance records
- View detailed reports

### Student Login
- Use USN as username
- View attendance percentage for all subjects
- Check attendance status with color-coded indicators
- Track attendance history

## Contributing

1. Fork the repository
2. Create a new branch
3. Make your changes
4. Submit a pull request

