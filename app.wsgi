#!/usr/bin/env python
import sys

# Add the application directory to the Python path
app_dir = '/var/www/pbxapi'
if app_dir not in sys.path:
    sys.path.insert(0, app_dir)

# Import the Flask app
# Database configuration is handled in db_config.py
from app import app as application