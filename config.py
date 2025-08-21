import os
from dotenv import load_dotenv

load_dotenv()

# Get the directory where this config file is located
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    # Database connection string - defaults to SQLite database file in project directory
    # This creates a file called 'assignment.db' that you can see in your project folder
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or f'sqlite:///{os.path.join(basedir, "assignment.db")}'
    
    # Disable modification tracking to save resources
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Echo SQL queries in development mode for debugging
    SQLALCHEMY_ECHO = os.environ.get('FLASK_ENV') == 'development'