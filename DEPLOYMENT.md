# Production Deployment Guide

## Error Analysis & Solutions

### Error: RuntimeError: Either 'SQLALCHEMY_DATABASE_URI' or 'SQLALCHEMY_BINDS' must be set

**Root Cause**: The production environment was missing proper database configuration.

**Solutions Implemented**:
1. Created `app.wsgi` file for proper WSGI deployment
2. Enhanced configuration with production-ready error handling
3. Added environment variable validation
4. Created production environment template

## Deployment Steps

### 1. Server Setup

Copy these files to your production server at `/var/www/pbxapi/`:
- `app.py`
- `app.wsgi`
- `config.py`
- `models.py`
- `.env` (from `.env.production` template)
- All other application files

### 2. Environment Configuration

1. Copy the production environment template:
   ```bash
   cp .env.production .env
   ```

2. Edit `.env` file with your production values:
   ```bash
   nano .env
   ```

3. **IMPORTANT**: Update these values:
   - `SECRET_KEY`: Generate a secure random key
   - `DATABASE_URL`: Configure your production database
   - `FLASK_ENV`: Set to `production`

### 3. Database Setup Options

#### Option 1: SQLite (Default)
```bash
DATABASE_URL=sqlite:///assignment.db
```

#### Option 2: SQL Server (Recommended for 3CX)
```bash
DATABASE_URL=mssql+pyodbc://username:password@server/database?driver=ODBC+Driver+17+for+SQL+Server
```

#### Option 3: PostgreSQL
```bash
DATABASE_URL=postgresql://username:password@localhost/database_name
```

### 4. Apache/WSGI Configuration

Ensure your Apache virtual host points to the WSGI file:
```apache
WSGIScriptAlias / /var/www/pbxapi/app.wsgi
WSGIDaemonProcess pbxapi python-path=/var/www/pbxapi
WSGIProcessGroup pbxapi
```

### 5. Permissions

Set proper permissions:
```bash
sudo chown -R www-data:www-data /var/www/pbxapi/
sudo chmod -R 755 /var/www/pbxapi/
```

### 6. Initialize Database

```bash
cd /var/www/pbxapi
python3 -c "from app import app, db; app.app_context().push(); db.create_all()"
```

## Security Checklist

- [ ] `SECRET_KEY` is set to a secure random value
- [ ] `FLASK_DEBUG=False` in production
- [ ] `FLASK_ENV=production`
- [ ] Database credentials are secure
- [ ] File permissions are properly set
- [ ] SSL/HTTPS is configured

## Troubleshooting

### Database Connection Issues
1. Verify `DATABASE_URL` format
2. Check database server connectivity
3. Ensure database exists and user has permissions
4. Check firewall rules

### WSGI Import Errors
1. Verify Python path in `app.wsgi`
2. Check file permissions
3. Ensure virtual environment is activated
4. Verify all dependencies are installed

### Configuration Errors
1. Check `.env` file exists and is readable
2. Verify environment variable names
3. Check for typos in configuration values

## Monitoring & Logs

Application logs will be written to Apache error logs. Monitor:
```bash
tail -f /var/log/apache2/error.log
```

For application-specific logs, check the Flask application logs in the configured log directory.