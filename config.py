import os
import logging

logger = logging.getLogger('3cx_server.config')

try:
    from db_config import MSSQL_DATABASE_URL
except ImportError as e:
    logger.critical("=" * 80)
    logger.critical("DATABASE CONFIGURATION ERROR")
    logger.critical("=" * 80)
    logger.critical("Failed to import database configuration from db_config.py")
    logger.critical("Error: %s", str(e))
    logger.critical("Please ensure db_config.py exists and is properly configured.")
    logger.critical("=" * 80)
    raise RuntimeError("Database configuration file missing or invalid") from e

class Config:
    """Application configuration for MS SQL Server."""

    def __init__(self):
        self._validate_database_url()

    def _validate_database_url(self):
        """Validate that the database URL has been configured."""
        if not MSSQL_DATABASE_URL or MSSQL_DATABASE_URL == "mssql+pyodbc://username:password@server/database?driver=ODBC+Driver+17+for+SQL+Server":
            logger.critical("=" * 80)
            logger.critical("DATABASE CONFIGURATION ERROR")
            logger.critical("=" * 80)
            logger.critical("The database URL has not been configured!")
            logger.critical("Please edit db_config.py and set your MS SQL database URL.")
            logger.critical("Current value: %s", MSSQL_DATABASE_URL)
            logger.critical("=" * 80)
            raise RuntimeError(
                "Database URL not configured. Please edit db_config.py with your MS SQL connection string."
            )

        # Check if it's a valid MS SQL connection string format
        if not MSSQL_DATABASE_URL.startswith('mssql+pyodbc://'):
            logger.critical("=" * 80)
            logger.critical("INVALID DATABASE URL FORMAT")
            logger.critical("=" * 80)
            logger.critical("The database URL must be a MS SQL connection string.")
            logger.critical("Expected format: mssql+pyodbc://username:password@server/database?driver=...")
            logger.critical("Current value: %s", MSSQL_DATABASE_URL)
            logger.critical("=" * 80)
            raise RuntimeError(
                "Invalid database URL format. Must start with 'mssql+pyodbc://'"
            )

    # MS SQL Database connection string
    SQLALCHEMY_DATABASE_URI = MSSQL_DATABASE_URL

    # Disable modification tracking to save resources
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Disable SQL echo in production
    SQLALCHEMY_ECHO = False

    # Security configurations
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    PREFERRED_URL_SCHEME = 'https'