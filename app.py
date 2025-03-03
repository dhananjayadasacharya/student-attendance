from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash, check_password_hash
import os
from dotenv import load_dotenv
from datetime import datetime
from pythonanywhere_config import MYSQL_CONFIG, APP_CONFIG

app = Flask(__name__)

# Load environment variables
load_dotenv()

# MySQL Configuration
app.config.update(MYSQL_CONFIG)

# Initialize MySQL
mysql = MySQL(app)

# Secret key for session
app.secret_key = APP_CONFIG['SECRET_KEY']

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        try:
            user_type = request.form.get('user_type')
            username = request.form.get('username')
            password = request.form.get('password')
            
            cur = mysql.connection.cursor()
            
            if user_type == 'faculty':
                cur.execute("SELECT * FROM faculty WHERE faculty_username = %s", [username])
                user = cur.fetchone()
                if user and check_password_hash(user['password'], password):
                    session['user_id'] = user['faculty_id']
                    session['user_type'] = 'faculty'
                    session['name'] = user['name']
                    return redirect(url_for('faculty_dashboard'))
            else:
                cur.execute("SELECT * FROM student WHERE usn = %s", [username])
                user = cur.fetchone()
                if user and check_password_hash(user['password'], password):
                    session['user_id'] = user['stu_id']
                    session['user_type'] = 'student'
                    session['name'] = user['name']
                    session['usn'] = user['usn']
                    return redirect(url_for('student_dashboard'))
            
            flash('Invalid username or password')
            return redirect(url_for('login'))
        except Exception as e:
            print(f"Error: {str(e)}")
            flash('An error occurred during login')
            return redirect(url_for('login'))
        finally:
            cur.close()
    
    return render_template('login.html')

@app.route('/faculty/dashboard')
def faculty_dashboard():
    if 'user_id' not in session or session['user_type'] != 'faculty':
        return redirect(url_for('login'))
    
    try:
        cur = mysql.connection.cursor()
        # Get subjects taught by the faculty along with their classes
        cur.execute("""
            SELECT DISTINCT s.subject_id, s.subject_name, c.class_id, c.name as class_name 
            FROM subject s 
            JOIN class_subject cs ON s.subject_id = cs.subject_id
            JOIN class c ON cs.class_id = c.class_id
            WHERE s.faculty_id = %s
            ORDER BY c.name, s.subject_name
        """, [session['user_id']])
        subjects = cur.fetchall()
        return render_template('faculty_dashboard.html', subjects=subjects)
    except Exception as e:
        print(f"Error: {str(e)}")
        flash('An error occurred while loading the dashboard')
        return redirect(url_for('login'))
    finally:
        cur.close()

@app.route('/student/dashboard')
def student_dashboard():
    if 'user_id' not in session or session['user_type'] != 'student':
        return redirect(url_for('login'))
    
    try:
        cur = mysql.connection.cursor()
        # Get student's class_id
        cur.execute("SELECT class_id FROM student WHERE stu_id = %s", [session['user_id']])
        student = cur.fetchone()
        if not student:
            flash('Student record not found')
            return redirect(url_for('login'))
            
        class_id = student['class_id']

        # Get attendance summary for subjects in student's class
        cur.execute("""
            SELECT 
                s.subject_name, 
                COALESCE(COUNT(CASE WHEN a.status = 'Present' THEN 1 END), 0) as present_count,
                COALESCE(COUNT(a.status), 0) as total_classes,
                CASE 
                    WHEN COUNT(a.status) > 0 
                    THEN (COUNT(CASE WHEN a.status = 'Present' THEN 1 END) * 100.0 / COUNT(a.status))
                    ELSE 0 
                END as attendance_percentage
            FROM subject s
            JOIN class_subject cs ON s.subject_id = cs.subject_id
            LEFT JOIN attendance a ON s.subject_id = a.subject_id AND a.stu_id = %s
            WHERE cs.class_id = %s
            GROUP BY s.subject_id, s.subject_name
        """, [session['user_id'], class_id])
        attendance_data = cur.fetchall()

        # Get absent dates for each subject
        cur.execute("""
            SELECT s.subject_name, a.date
            FROM attendance a
            JOIN subject s ON a.subject_id = s.subject_id
            WHERE a.stu_id = %s AND a.status = 'Absent'
            ORDER BY a.date DESC
        """, [session['user_id']])
        absent_dates = cur.fetchall()

        return render_template('student_dashboard.html', 
                             attendance_data=attendance_data,
                             absent_dates=absent_dates)
    except Exception as e:
        print(f"Error: {str(e)}")
        flash('An error occurred while loading the dashboard')
        return redirect(url_for('login'))
    finally:
        cur.close()

@app.route('/faculty/take-attendance', methods=['GET', 'POST'])
def take_attendance():
    if 'user_id' not in session or session['user_type'] != 'faculty':
        return redirect(url_for('login'))
    
    try:
        cur = mysql.connection.cursor()
        
        if request.method == 'POST':
            subject_id = request.form.get('subject_id')
            class_id = request.form.get('class_id')
            attendance_data = request.form.getlist('attendance')
            date = datetime.now().date()
            
            # Validate inputs
            if not all([subject_id, class_id]):
                flash('Missing required fields', 'danger')
                return redirect(url_for('faculty_dashboard'))
            
            # Check if faculty teaches this subject
            cur.execute("""
                SELECT COUNT(*) as count 
                FROM subject 
                WHERE subject_id = %s AND faculty_id = %s
            """, [subject_id, session['user_id']])
            result = cur.fetchone()
            if result['count'] == 0:
                flash('You are not authorized to take attendance for this subject', 'danger')
                return redirect(url_for('faculty_dashboard'))
            
            # Check if attendance already exists
            cur.execute("""
                SELECT COUNT(*) as count 
                FROM attendance 
                WHERE subject_id = %s AND class_id = %s AND date = %s
            """, [subject_id, class_id, date])
            result = cur.fetchone()
            
            if result['count'] > 0:
                flash('Attendance for this subject and date already exists', 'warning')
                return redirect(url_for('faculty_dashboard'))
            
            # Get all students in the class
            cur.execute("SELECT stu_id FROM student WHERE class_id = %s", [class_id])
            students = cur.fetchall()
            
            if not students:
                flash('No students found in this class', 'warning')
                return redirect(url_for('faculty_dashboard'))
            
            # Record attendance for each student
            for student in students:
                status = 'Present' if str(student['stu_id']) in attendance_data else 'Absent'
                cur.execute("""
                    INSERT INTO attendance (stu_id, class_id, subject_id, date, status)
                    VALUES (%s, %s, %s, %s, %s)
                """, [student['stu_id'], class_id, subject_id, date, status])
            
            mysql.connection.commit()
            flash('Attendance recorded successfully', 'success')
            return redirect(url_for('faculty_dashboard'))
        
        # For GET request, show the attendance form
        subject_id = request.args.get('subject_id')
        class_id = request.args.get('class_id')
        
        if not all([subject_id, class_id]):
            flash('Missing required parameters', 'danger')
            return redirect(url_for('faculty_dashboard'))
        
        # Get class and subject details
        cur.execute("""
            SELECT s.subject_name, c.name as class_name
            FROM subject s
            JOIN class c ON c.class_id = %s
            WHERE s.subject_id = %s AND s.faculty_id = %s
        """, [class_id, subject_id, session['user_id']])
        class_info = cur.fetchone()
        
        if not class_info:
            flash('Invalid subject or class selection', 'danger')
            return redirect(url_for('faculty_dashboard'))
        
        # Get students in the class
        cur.execute("""
            SELECT stu_id, usn, name
            FROM student
            WHERE class_id = %s
            ORDER BY usn
        """, [class_id])
        students = cur.fetchall()
        
        if not students:
            flash('No students found in this class', 'warning')
            return redirect(url_for('faculty_dashboard'))
        
        return render_template('take_attendance.html', 
                             students=students, 
                             subject_id=subject_id,
                             class_id=class_id,
                             class_info=class_info,
                             datetime=datetime)
    
    except Exception as e:
        print(f"Error in take_attendance: {str(e)}")
        flash('An error occurred while processing attendance', 'danger')
        return redirect(url_for('faculty_dashboard'))
    finally:
        cur.close()

@app.route('/faculty/edit-attendance', methods=['GET', 'POST'])
def edit_attendance():
    if 'user_id' not in session or session['user_type'] != 'faculty':
        return redirect(url_for('login'))
    
    try:
        cur = mysql.connection.cursor()
        
        if request.method == 'POST':
            subject_id = request.form.get('subject_id')
            class_id = request.form.get('class_id')
            date = request.form.get('date')
            attendance_data = request.form.getlist('attendance')
            
            # Update attendance for each student
            cur.execute("SELECT stu_id FROM student WHERE class_id = %s", [class_id])
            students = cur.fetchall()
            
            for student in students:
                status = 'Present' if str(student['stu_id']) in attendance_data else 'Absent'
                cur.execute("""
                    UPDATE attendance 
                    SET status = %s
                    WHERE stu_id = %s AND class_id = %s AND subject_id = %s AND date = %s
                """, [status, student['stu_id'], class_id, subject_id, date])
            
            mysql.connection.commit()
            flash('Attendance updated successfully')
            return redirect(url_for('faculty_dashboard'))
        
        # For GET request, show the edit form
        subject_id = request.args.get('subject_id')
        class_id = request.args.get('class_id')
        date = request.args.get('date')
        
        # Get class and subject details
        cur.execute("""
            SELECT s.subject_name, c.name as class_name
            FROM subject s
            JOIN class c ON c.class_id = %s
            WHERE s.subject_id = %s
        """, [class_id, subject_id])
        class_info = cur.fetchone()
        
        # Get students with their attendance status
        cur.execute("""
            SELECT s.stu_id, s.usn, s.name, a.status
            FROM student s
            LEFT JOIN attendance a ON s.stu_id = a.stu_id 
                AND a.subject_id = %s 
                AND a.class_id = %s 
                AND a.date = %s
            WHERE s.class_id = %s
            ORDER BY s.usn
        """, [subject_id, class_id, date, class_id])
        students = cur.fetchall()
        
        return render_template('edit_attendance.html', 
                             students=students,
                             subject_id=subject_id,
                             class_id=class_id,
                             date=date,
                             class_info=class_info)
    
    except Exception as e:
        print(f"Error: {str(e)}")
        flash('An error occurred while processing attendance')
        return redirect(url_for('faculty_dashboard'))
    finally:
        cur.close()

@app.route('/faculty/view-reports')
def view_reports():
    if 'user_id' not in session or session['user_type'] != 'faculty':
        return redirect(url_for('login'))
    
    subject_id = request.args.get('subject_id')
    report_type = request.args.get('report_type')
    
    cur = mysql.connection.cursor()
    
    if report_type == 'class':
        cur.execute("""
            SELECT s.name, s.usn,
                   COUNT(CASE WHEN a.status = 'Present' THEN 1 END) as present_count,
                   COUNT(a.status) as total_classes,
                   (COUNT(CASE WHEN a.status = 'Present' THEN 1 END) * 100.0 / NULLIF(COUNT(a.status), 0)) as attendance_percentage
            FROM student s
            LEFT JOIN attendance a ON s.stu_id = a.stu_id
            WHERE a.subject_id = %s
            GROUP BY s.stu_id, s.name, s.usn
            ORDER BY attendance_percentage DESC
        """, [subject_id])
    else:
        student_id = request.args.get('student_id')
        cur.execute("""
            SELECT a.date, a.status
            FROM attendance a
            WHERE a.subject_id = %s AND a.stu_id = %s
            ORDER BY a.date DESC
        """, [subject_id, student_id])
    
    report_data = cur.fetchall()
    
    return render_template('view_reports.html', 
                         report_data=report_data, 
                         report_type=report_type)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True) 