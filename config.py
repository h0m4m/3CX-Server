import os
import logging
from dotenv import load_dotenv

# Load environment variables from .env file if it exists
load_dotenv()

# Get the directory where this config file is located
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    """Application configuration class with production-ready error handling."""

    def __init__(self):
        self._validate_environment()

    def _validate_environment(self):
        """Validate that required environment variables are set."""
        database_uri = self.SQLALCHEMY_DATABASE_URI
        if not database_uri:
            error_msg = (
                "Database configuration error: SQLALCHEMY_DATABASE_URI is not set. "
                "Please ensure DATABASE_URL environment variable is configured or "
                "the default SQLite path is accessible."
            )
            logging.error(error_msg)
            raise RuntimeError(error_msg)

    # Database connection string with production-ready fallback
    @property
    def SQLALCHEMY_DATABASE_URI(self):
        """Get database URI with proper fallback handling."""
        database_url = os.environ.get('DATABASE_URL')

        # If DATABASE_URL is not set, use SQLite as fallback
        if not database_url:
            sqlite_path = os.path.join(basedir, "assignment.db")
            database_url = f'sqlite:///{sqlite_path}'

            # Log the fallback in production
            if os.environ.get('FLASK_ENV') == 'production':
                logging.warning(f"Using SQLite fallback database at: {sqlite_path}")

        return database_url

    # Disable modification tracking to save resources
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Echo SQL queries in development mode for debugging
    @property
    def SQLALCHEMY_ECHO(self):
        return os.environ.get('FLASK_ENV') == 'development'

    # Additional production configurations
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'

    # Security configurations for production
    @property
    def PREFERRED_URL_SCHEME(self):
        return 'https' if os.environ.get('FLASK_ENV') == 'production' else 'http'