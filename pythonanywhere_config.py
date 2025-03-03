import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# PythonAnywhere MySQL Configuration
MYSQL_CONFIG = {
    'MYSQL_HOST': os.getenv('MYSQL_HOST', 'your-username.mysql.pythonanywhere-services.com'),
    'MYSQL_USER': os.getenv('MYSQL_USER', 'your-username'),
    'MYSQL_PASSWORD': os.getenv('MYSQL_PASSWORD', 'your-password'),
    'MYSQL_DB': os.getenv('MYSQL_DB', 'your-username$attendance'),
    'MYSQL_CURSORCLASS': 'DictCursor'
}

# Application configuration
APP_CONFIG = {
    'SECRET_KEY': os.getenv('SECRET_KEY', os.urandom(24)),
    'DEBUG': False  # Set to False in production
} 