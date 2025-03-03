from flask import Flask, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
import mysql.connector
from functools import wraps
import os
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Database configuration from environment variables
db_config = {
    'host': os.getenv('MYSQL_HOST'),
    'port': int(os.getenv('MYSQL_PORT', 3306)),
    'user': os.getenv('MYSQL_USER'),
    'password': os.getenv('MYSQL_PASSWORD'),
    'database': os.getenv('MYSQL_DB')
}

def get_db():
    try:
        connection = mysql.connector.connect(**db_config)
        return connection
    except mysql.connector.Error as err:
        print(f"Database connection error: {err}")
        return None

def init_db():
    """Initialize the database with required tables"""
    try:
        conn = get_db()
        if conn:
            cursor = conn.cursor()
            
            # Disable foreign key checks temporarily
            cursor.execute("SET FOREIGN_KEY_CHECKS = 0")
            
            # Create tables
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS class (
                    class_id INT PRIMARY KEY AUTO_INCREMENT,
                    name VARCHAR(50) NOT NULL,
                    department VARCHAR(50) NOT NULL
                )
            """)
            
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS faculty (
                    faculty_id INT PRIMARY KEY AUTO_INCREMENT,
                    name VARCHAR(100) NOT NULL,
                    faculty_username VARCHAR(50) UNIQUE NOT NULL,
                    password VARCHAR(255) NOT NULL,
                    department VARCHAR(50) NOT NULL
                )
            """)
            
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS subject (
                    subject_id INT PRIMARY KEY AUTO_INCREMENT,
                    name VARCHAR(100) NOT NULL,
                    subject_code VARCHAR(20) UNIQUE NOT NULL
                )
            """)
            
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS student (
                    stu_id INT PRIMARY KEY AUTO_INCREMENT,
                    name VARCHAR(100) NOT NULL,
                    usn VARCHAR(20) UNIQUE NOT NULL,
                    password VARCHAR(255) NOT NULL,
                    class_id INT,
                    FOREIGN KEY (class_id) REFERENCES class(class_id)
                )
            """)
            
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS class_subjects (
                    class_id INT,
                    subject_id INT,
                    faculty_id INT,
                    PRIMARY KEY (class_id, subject_id),
                    FOREIGN KEY (class_id) REFERENCES class(class_id),
                    FOREIGN KEY (subject_id) REFERENCES subject(subject_id),
                    FOREIGN KEY (faculty_id) REFERENCES faculty(faculty_id)
                )
            """)
            
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS attendance (
                    attendance_id INT PRIMARY KEY AUTO_INCREMENT,
                    stu_id INT,
                    class_id INT,
                    subject_id INT,
                    date DATE NOT NULL,
                    status ENUM('Present', 'Absent') NOT NULL,
                    FOREIGN KEY (stu_id) REFERENCES student(stu_id),
                    FOREIGN KEY (class_id) REFERENCES class(class_id),
                    FOREIGN KEY (subject_id) REFERENCES subject(subject_id)
                )
            """)
            
            # Re-enable foreign key checks
            cursor.execute("SET FOREIGN_KEY_CHECKS = 1")
            
            conn.commit()
            print("Database initialized successfully")
            
    except mysql.connector.Error as err:
        print(f"Error initializing database: {err}")
        if conn:
            conn.rollback()
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user_type = request.form['user_type']
        
        db = get_db()
        cursor = db.cursor(dictionary=True)
        
        if user_type == 'faculty':
            cursor.execute("SELECT * FROM faculty WHERE faculty_username = %s", [username])
        else:
            cursor.execute("SELECT * FROM student WHERE usn = %s", [username])
            
        user = cursor.fetchone()
        
        if user and check_password_hash(user['password'], password):
            session['user_id'] = user['faculty_id' if user_type == 'faculty' else 'stu_id']
            session['user_type'] = user_type
            session['username'] = username
            return redirect(url_for('dashboard'))
            
        flash('Invalid credentials')
    return render_template('login.html')

@app.route('/dashboard')
@login_required
def dashboard():
    db = get_db()
    cursor = db.cursor(dictionary=True)
    
    if session['user_type'] == 'faculty':
        # Get faculty's subjects and classes
        cursor.execute("""
            SELECT s.name as subject_name, c.name as class_name, cs.class_id, cs.subject_id
            FROM class_subjects cs
            JOIN subject s ON cs.subject_id = s.subject_id
            JOIN class c ON cs.class_id = c.class_id
            WHERE cs.faculty_id = %s
        """, [session['user_id']])
        classes = cursor.fetchall()
        return render_template('faculty_dashboard.html', classes=classes)
    else:
        # Get student's attendance
        cursor.execute("""
            SELECT s.name as subject_name, 
                   COUNT(CASE WHEN a.status = 'Present' THEN 1 END) as present_count,
                   COUNT(*) as total_classes,
                   ROUND(COUNT(CASE WHEN a.status = 'Present' THEN 1 END) * 100.0 / COUNT(*), 2) as attendance_percentage
            FROM attendance a
            JOIN subject s ON a.subject_id = s.subject_id
            WHERE a.stu_id = %s
            GROUP BY s.subject_id, s.name
        """, [session['user_id']])
        attendance = cursor.fetchall()
        return render_template('student_dashboard.html', attendance=attendance)

@app.route('/take_attendance/<int:class_id>/<int:subject_id>', methods=['GET', 'POST'])
@login_required
def take_attendance(class_id, subject_id):
    if session['user_type'] != 'faculty':
        return redirect(url_for('dashboard'))
        
    db = get_db()
    cursor = db.cursor(dictionary=True)
    
    if request.method == 'POST':
        date = datetime.now().date()
        for student_id, status in request.form.items():
            if student_id.startswith('student_'):
                stu_id = int(student_id.split('_')[1])
                cursor.execute("""
                    INSERT INTO attendance (stu_id, class_id, subject_id, date, status)
                    VALUES (%s, %s, %s, %s, %s)
                """, [stu_id, class_id, subject_id, date, status])
        db.commit()
        flash('Attendance recorded successfully')
        return redirect(url_for('dashboard'))
    
    # Get students in the class
    cursor.execute("""
        SELECT stu_id, name, usn
        FROM student
        WHERE class_id = %s
        ORDER BY usn
    """, [class_id])
    students = cursor.fetchall()
    
    return render_template('take_attendance.html', students=students, class_id=class_id, subject_id=subject_id)

@app.route('/view_attendance/<int:class_id>/<int:subject_id>')
@login_required
def view_attendance(class_id, subject_id):
    if session['user_type'] != 'faculty':
        return redirect(url_for('dashboard'))
        
    db = get_db()
    cursor = db.cursor(dictionary=True)
    
    cursor.execute("""
        SELECT s.name, s.usn,
               COUNT(CASE WHEN a.status = 'Present' THEN 1 END) as present_count,
               COUNT(*) as total_classes,
               ROUND(COUNT(CASE WHEN a.status = 'Present' THEN 1 END) * 100.0 / COUNT(*), 2) as attendance_percentage
        FROM student s
        LEFT JOIN attendance a ON s.stu_id = a.stu_id AND a.subject_id = %s
        WHERE s.class_id = %s
        GROUP BY s.stu_id, s.name, s.usn
        ORDER BY s.usn
    """, [subject_id, class_id])
    attendance = cursor.fetchall()
    
    return render_template('view_attendance.html', attendance=attendance)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

if __name__ == '__main__':
    init_db()  # Initialize database tables
    app.run(debug=True) 