from app import get_db
from werkzeug.security import generate_password_hash
import mysql.connector

def add_test_data():
    conn = None
    try:
        conn = get_db()
        if conn:
            cursor = conn.cursor()
            
            # Disable foreign key checks temporarily
            cursor.execute("SET FOREIGN_KEY_CHECKS = 0")
            
            # Clear existing data
            tables = ['attendance', 'class_subjects', 'student', 'subject', 'faculty', 'class']
            for table in tables:
                cursor.execute(f"TRUNCATE TABLE {table}")
            
            # Add classes
            cursor.execute("""
                INSERT INTO class (name, department) VALUES
                ('ISE-A', 'Information Science'),
                ('ISE-B', 'Information Science')
            """)
            
            # Add faculty
            hashed_password = generate_password_hash('password123')
            cursor.execute("""
                INSERT INTO faculty (name, faculty_username, password, department) VALUES
                ('Dr. Rajesh Kumar', 'rajesh_k', %s, 'Information Science'),
                ('Prof. Priya Singh', 'priya_s', %s, 'Information Science')
            """, [hashed_password, hashed_password])
            
            # Add subjects
            cursor.execute("""
                INSERT INTO subject (name, subject_code) VALUES
                ('ATCD', 'CS201'),
                ('Computer Networks', 'CS202'),
                ('Discrete Mathematics', 'CS203'),
                ('Python Programming', 'CS204')
            """)
            
            # Get IDs for mapping
            cursor.execute("SELECT class_id FROM class WHERE name = 'ISE-A'")
            ise_a_id = cursor.fetchone()[0]
            
            cursor.execute("SELECT faculty_id FROM faculty WHERE faculty_username = 'rajesh_k'")
            rajesh_id = cursor.fetchone()[0]
            
            cursor.execute("SELECT subject_id FROM subject WHERE subject_code = 'CS201'")
            atcd_id = cursor.fetchone()[0]
            
            # Map classes and subjects
            cursor.execute("""
                INSERT INTO class_subjects (class_id, subject_id, faculty_id)
                VALUES (%s, %s, %s)
            """, [ise_a_id, atcd_id, rajesh_id])
            
            # Add a test student
            cursor.execute("""
                INSERT INTO student (name, usn, password, class_id)
                VALUES ('John Doe', '1SI20IS001', %s, %s)
            """, [hashed_password, ise_a_id])
            
            # Re-enable foreign key checks
            cursor.execute("SET FOREIGN_KEY_CHECKS = 1")
            
            conn.commit()
            print("Test data added successfully")
            
    except mysql.connector.Error as e:
        print(f"Error adding test data: {e}")
        if conn:
            conn.rollback()
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

if __name__ == '__main__':
    add_test_data() 