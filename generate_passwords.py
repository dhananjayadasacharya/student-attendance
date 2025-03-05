from werkzeug.security import generate_password_hash
import mysql.connector

# Database connection
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="#1Parandhama",
    database="attendance"
)
cursor = db.cursor()

# Generate password hash
password = "12345678"
hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

# Update faculty passwords
cursor.execute("UPDATE faculty SET password = %s", [hashed_password])

# Update student passwords
cursor.execute("UPDATE student SET password = %s", [hashed_password])

# Commit changes
db.commit()

print("Passwords updated successfully!")
cursor.close()
db.close() 