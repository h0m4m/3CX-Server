#!/usr/bin/env python
import sys
import os

# Add the application directory to the Python path
app_dir = '/var/www/pbxapi'
if app_dir not in sys.path:
    sys.path.insert(0, app_dir)

# Set environment variables if .env file exists
env_file = os.path.join(app_dir, '.env')
if os.path.exists(env_file):
    from dotenv import load_dotenv
    load_dotenv(env_file)

# Ensure the application runs in production mode
if not os.environ.get('FLASK_ENV'):
    os.environ['FLASK_ENV'] = 'production'

# Import the Flask app
from app import app as application