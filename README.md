# Student Attendance Management System

A Flask-based web application for managing student attendance with MySQL database integration.

## Features

- Faculty Management
- Student Management
- Attendance Tracking
- Secure Authentication
- Reports Generation

## Tech Stack

- Python 3.8+
- Flask 2.0.1
- MySQL
- Bootstrap 5

## Installation

1. Clone the repository
```bash
git clone https://github.com/yourusername/student-attendance.git
cd student-attendance
```

2. Create virtual environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Set up environment variables in `.env`:
```
MYSQL_HOST=your_host
MYSQL_PORT=3306
MYSQL_USER=your_user
MYSQL_PASSWORD=your_password
MYSQL_DB=your_database
FLASK_ENV=development
FLASK_APP=app.py
```

5. Initialize database and add test data
```bash
python app.py
python init_data.py
```

## Test Credentials

### Faculty Login
- Username: rajesh_k
- Password: password123

### Student Login
- USN: 1SI20IS001
- Password: password123

## Project Structure

```
student-attendance/
├── app.py              # Main application file
├── init_data.py        # Database initialization script
├── requirements.txt    # Python dependencies
├── flask_app.py        # WSGI entry point
├── templates/          # HTML templates
└── static/            # Static files (CSS, JS, images)
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details. 