import tkinter as tk
from tkinter import ttk, messagebox
from werkzeug.security import generate_password_hash
import mysql.connector
from mysql.connector import Error

def connect_db():
    try:
        db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="#1Parandhama",
            database="attendance"
        )
        return db
    except Error as e:
        messagebox.showerror("Database Error", f"Error connecting to database: {e}")
        return None

def add_faculty(name, username, password, department):
    """Add a new faculty member with hashed password"""
    try:
        db = connect_db()
        if not db:
            return False
        
        cursor = db.cursor()
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        
        # Check if username already exists
        cursor.execute("SELECT faculty_id FROM faculty WHERE faculty_username = %s", [username])
        if cursor.fetchone():
            messagebox.showerror("Error", f"Faculty username '{username}' already exists")
            return False
        
        # Insert new faculty
        sql = """INSERT INTO faculty (name, faculty_username, password, department) 
                 VALUES (%s, %s, %s, %s)"""
        cursor.execute(sql, [name, username, hashed_password, department])
        db.commit()
        
        messagebox.showinfo("Success", f"Faculty '{name}' added successfully with username '{username}'")
        return True
    except Error as e:
        messagebox.showerror("Error", f"Error adding faculty: {e}")
        return False
    finally:
        if db and db.is_connected():
            cursor.close()
            db.close()

def add_student(name, username, password, class_id):
    """Add a new student with hashed password"""
    try:
        db = connect_db()
        if not db:
            return False
        
        cursor = db.cursor()
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        
        # Check if usn already exists
        cursor.execute("SELECT stu_id FROM student WHERE usn = %s", [username])
        if cursor.fetchone():
            messagebox.showerror("Error", f"Student USN '{username}' already exists")
            return False
        
        # Verify class_id exists
        cursor.execute("SELECT class_id FROM class WHERE class_id = %s", [class_id])
        if not cursor.fetchone():
            messagebox.showerror("Error", f"Class ID {class_id} does not exist")
            return False
        
        # Insert new student using usn
        sql = """INSERT INTO student (name, usn, password, class_id) 
                 VALUES (%s, %s, %s, %s)"""
        cursor.execute(sql, [name, username, hashed_password, class_id])
        db.commit()
        
        messagebox.showinfo("Success", f"Student '{name}' added successfully with USN '{username}'")
        return True
    except Error as e:
        messagebox.showerror("Error", f"Error adding student: {e}")
        return False
    finally:
        if db and db.is_connected():
            cursor.close()
            db.close()

def reset_password(username, new_password, user_type='faculty'):
    """Reset password for existing user"""
    try:
        db = connect_db()
        if not db:
            return False
        
        cursor = db.cursor()
        hashed_password = generate_password_hash(new_password, method='pbkdf2:sha256')
        
        if user_type == 'faculty':
            sql = "UPDATE faculty SET password = %s WHERE faculty_username = %s"
            id_field = "faculty_username"
            table = "faculty"
        else:
            # Update student password query using usn
            sql = "UPDATE student SET password = %s WHERE usn = %s"
            id_field = "usn"
            table = "student"
        
        # Check if user exists
        cursor.execute(f"SELECT {id_field} FROM {table} WHERE {id_field} = %s", [username])
        if not cursor.fetchone():
            messagebox.showerror("Error", f"{user_type.capitalize()} {'USN' if user_type == 'student' else 'username'} '{username}' not found")
            return False
        
        cursor.execute(sql, [hashed_password, username])
        db.commit()
        
        messagebox.showinfo("Success", f"Password reset successfully for {user_type} '{username}'")
        return True
    except Error as e:
        messagebox.showerror("Error", f"Error resetting password: {e}")
        return False
    finally:
        if db and db.is_connected():
            cursor.close()
            db.close()

def get_class_names():
    """Get list of class names and IDs"""
    try:
        db = connect_db()
        if not db:
            return []
        
        cursor = db.cursor()
        cursor.execute("SELECT class_id, name FROM class ORDER BY class_id")
        return cursor.fetchall()
    except Error as e:
        messagebox.showerror("Error", f"Error fetching classes: {e}")
        return []
    finally:
        if db and db.is_connected():
            cursor.close()
            db.close()

class UserManagementApp:
    def __init__(self, root):
        self.root = root
        self.root.title("User Management System")
        self.root.geometry("600x400")
        
        # Create notebook for tabs
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(expand=True, fill='both', padx=10, pady=5)
        
        # Create tabs
        self.faculty_frame = ttk.Frame(self.notebook)
        self.student_frame = ttk.Frame(self.notebook)
        self.reset_frame = ttk.Frame(self.notebook)
        
        self.notebook.add(self.faculty_frame, text='Add Faculty')
        self.notebook.add(self.student_frame, text='Add Student')
        self.notebook.add(self.reset_frame, text='Reset Password')
        
        self.setup_faculty_tab()
        self.setup_student_tab()
        self.setup_reset_tab()
    
    def setup_faculty_tab(self):
        # Faculty tab
        ttk.Label(self.faculty_frame, text="Add New Faculty", font=('Helvetica', 14, 'bold')).pack(pady=10)
        
        form_frame = ttk.Frame(self.faculty_frame)
        form_frame.pack(padx=20, pady=10)
        
        # Name
        ttk.Label(form_frame, text="Full Name:").grid(row=0, column=0, padx=5, pady=5, sticky='e')
        self.faculty_name = ttk.Entry(form_frame, width=30)
        self.faculty_name.grid(row=0, column=1, padx=5, pady=5)
        
        # Username
        ttk.Label(form_frame, text="Username:").grid(row=1, column=0, padx=5, pady=5, sticky='e')
        self.faculty_username = ttk.Entry(form_frame, width=30)
        self.faculty_username.grid(row=1, column=1, padx=5, pady=5)
        
        # Password
        ttk.Label(form_frame, text="Password:").grid(row=2, column=0, padx=5, pady=5, sticky='e')
        self.faculty_password = ttk.Entry(form_frame, width=30, show="*")
        self.faculty_password.grid(row=2, column=1, padx=5, pady=5)
        
        # Department
        ttk.Label(form_frame, text="Department:").grid(row=3, column=0, padx=5, pady=5, sticky='e')
        self.faculty_dept = ttk.Entry(form_frame, width=30)
        self.faculty_dept.grid(row=3, column=1, padx=5, pady=5)
        
        # Submit button
        ttk.Button(form_frame, text="Add Faculty", 
                  command=self.submit_faculty).grid(row=4, column=0, columnspan=2, pady=20)
    
    def setup_student_tab(self):
        # Student tab
        ttk.Label(self.student_frame, text="Add New Student", font=('Helvetica', 14, 'bold')).pack(pady=10)
        
        form_frame = ttk.Frame(self.student_frame)
        form_frame.pack(padx=20, pady=10)
        
        # Name
        ttk.Label(form_frame, text="Full Name:").grid(row=0, column=0, padx=5, pady=5, sticky='e')
        self.student_name = ttk.Entry(form_frame, width=30)
        self.student_name.grid(row=0, column=1, padx=5, pady=5)
        
        # Username
        ttk.Label(form_frame, text="Username:").grid(row=1, column=0, padx=5, pady=5, sticky='e')
        self.student_username = ttk.Entry(form_frame, width=30)
        self.student_username.grid(row=1, column=1, padx=5, pady=5)
        
        # Password
        ttk.Label(form_frame, text="Password:").grid(row=2, column=0, padx=5, pady=5, sticky='e')
        self.student_password = ttk.Entry(form_frame, width=30, show="*")
        self.student_password.grid(row=2, column=1, padx=5, pady=5)
        
        # Class
        ttk.Label(form_frame, text="Class:").grid(row=3, column=0, padx=5, pady=5, sticky='e')
        self.class_var = tk.StringVar()
        self.class_combo = ttk.Combobox(form_frame, textvariable=self.class_var, width=27, state='readonly')
        self.class_combo.grid(row=3, column=1, padx=5, pady=5)
        
        # Populate class dropdown
        classes = get_class_names()
        self.class_combo['values'] = [f"{id} - {name}" for id, name in classes]
        
        # Submit button
        ttk.Button(form_frame, text="Add Student", 
                  command=self.submit_student).grid(row=4, column=0, columnspan=2, pady=20)
    
    def setup_reset_tab(self):
        # Reset password tab
        ttk.Label(self.reset_frame, text="Reset Password", font=('Helvetica', 14, 'bold')).pack(pady=10)
        
        form_frame = ttk.Frame(self.reset_frame)
        form_frame.pack(padx=20, pady=10)
        
        # User type
        ttk.Label(form_frame, text="User Type:").grid(row=0, column=0, padx=5, pady=5, sticky='e')
        self.user_type = tk.StringVar(value='faculty')
        ttk.Radiobutton(form_frame, text="Faculty", variable=self.user_type, 
                       value='faculty').grid(row=0, column=1, padx=5, pady=5)
        ttk.Radiobutton(form_frame, text="Student", variable=self.user_type, 
                       value='student').grid(row=0, column=2, padx=5, pady=5)
        
        # Username
        ttk.Label(form_frame, text="Username:").grid(row=1, column=0, padx=5, pady=5, sticky='e')
        self.reset_username = ttk.Entry(form_frame, width=30)
        self.reset_username.grid(row=1, column=1, columnspan=2, padx=5, pady=5)
        
        # New password
        ttk.Label(form_frame, text="New Password:").grid(row=2, column=0, padx=5, pady=5, sticky='e')
        self.reset_password = ttk.Entry(form_frame, width=30, show="*")
        self.reset_password.grid(row=2, column=1, columnspan=2, padx=5, pady=5)
        
        # Submit button
        ttk.Button(form_frame, text="Reset Password", 
                  command=self.submit_reset).grid(row=3, column=0, columnspan=3, pady=20)
    
    def submit_faculty(self):
        name = self.faculty_name.get().strip()
        username = self.faculty_username.get().strip()
        password = self.faculty_password.get()
        department = self.faculty_dept.get().strip()
        
        if not all([name, username, password, department]):
            messagebox.showerror("Error", "All fields are required")
            return
        
        if add_faculty(name, username, password, department):
            # Clear fields on success
            self.faculty_name.delete(0, tk.END)
            self.faculty_username.delete(0, tk.END)
            self.faculty_password.delete(0, tk.END)
            self.faculty_dept.delete(0, tk.END)
    
    def submit_student(self):
        name = self.student_name.get().strip()
        username = self.student_username.get().strip()
        password = self.student_password.get()
        class_selection = self.class_var.get()
        
        if not all([name, username, password, class_selection]):
            messagebox.showerror("Error", "All fields are required")
            return
        
        try:
            class_id = int(class_selection.split(' - ')[0])
        except (ValueError, IndexError):
            messagebox.showerror("Error", "Please select a valid class")
            return
        
        if add_student(name, username, password, class_id):
            # Clear fields on success
            self.student_name.delete(0, tk.END)
            self.student_username.delete(0, tk.END)
            self.student_password.delete(0, tk.END)
            self.class_var.set('')
    
    def submit_reset(self):
        username = self.reset_username.get().strip()
        password = self.reset_password.get()
        user_type = self.user_type.get()
        
        if not all([username, password]):
            messagebox.showerror("Error", "All fields are required")
            return
        
        if reset_password(username, password, user_type):
            # Clear fields on success
            self.reset_username.delete(0, tk.END)
            self.reset_password.delete(0, tk.END)

def main():
    root = tk.Tk()
    app = UserManagementApp(root)
    root.mainloop()

if __name__ == '__main__':
    main() 