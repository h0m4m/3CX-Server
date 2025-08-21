# Flask Assignment API

A simple Flask API with SQLite database for managing contact assignments via webhooks. The database appears as a file (`assignment.db`) in your project directory.

## Features

- Flask REST API with webhook endpoint
- SQLite database (visible as `assignment.db` file in your project)
- **Database-agnostic**: Switch to PostgreSQL or MS SQL by only changing connection string
- Automatic create/update of assignment records based on phone number
- SQLAlchemy ORM for complete database portability

## Database Schema

**Table: `assignment`**
- `id` (Primary Key)
- `customer_phone` (String, Unique) - Format: +60123456789
- `assignee` (String) - Name like "John Doe"
- `created_at` (DateTime)
- `updated_at` (DateTime)

## Prerequisites

- Python 3.8 or higher
- No database installation needed (SQLite is built into Python)

## Where is the Database?

**SQLite creates a file called `assignment.db` directly in your project folder!**

You'll see it appear after running the app:
```
3CX-Server/
├── app.py
├── models.py
├── assignment.db  <-- YOUR DATABASE FILE IS HERE!
└── ...
```

## Setup Instructions

### 1. Setup Virtual Environment and Dependencies

```bash
# Virtual environment is already created
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Dependencies are already installed via:
# pip install -r requirements.txt
```

### 2. Configure Environment

The `.env` file is already created with default settings:
```bash
# SQLite - creates assignment.db file in project directory
DATABASE_URL=sqlite:///assignment.db
FLASK_ENV=development
FLASK_DEBUG=True
```

### 3. Initialize Database Tables

```bash
# Create tables and add sample data
python init_db.py
```

### 4. Run the Application

```bash
# Start the Flask server (default port 8000)
python app.py

# Or specify a custom port:
PORT=3000 python app.py
```

The API will be available at `http://localhost:8000`

## API Endpoints

### Health Check
```bash
GET /health
```

### Webhook Endpoint
```bash
POST /webhook/contact
Content-Type: application/json

{
  "contact": {
    "id": 1,
    "firstName": "John",
    "lastName": "Doe",
    "phone": "+60123456789",
    "email": "johndoe@sample.com",
    "assignee": {
      "id": 2,
      "firstName": "Jane",
      "lastName": "Smith",
      "email": "janesmith@sample.com"
    }
  },
  "event_type": "contact.assignee.updated",
  "event_id": "e8e3d4a4-5128-4f7a-89b9-fb188e3898e7"
}
```

### Get All Assignments
```bash
GET /assignments
```

### Get Assignment by Phone
```bash
GET /assignments/+60123456789
# or
GET /assignments/60123456789
```

## Testing the Webhook

```bash
# Create or update an assignment
curl -X POST http://localhost:8000/webhook/contact \
  -H "Content-Type: application/json" \
  -d '{
    "contact": {
      "phone": "+60123456789",
      "assignee": {
        "firstName": "John",
        "lastName": "Doe"
      }
    },
    "event_type": "contact.assignee.updated"
  }'

# Get all assignments
curl http://localhost:8000/assignments

# Get specific assignment
curl http://localhost:8000/assignments/+60123456789
```

## Switching to Other Databases (NO CODE CHANGES!)

**The code is 100% database-agnostic thanks to SQLAlchemy ORM!**

### For MS SQL Server:

1. Install the MS SQL driver:
```bash
pip install pyodbc
```

2. Update ONLY the `.env` file:
```
DATABASE_URL=mssql+pyodbc://username:password@server/database?driver=ODBC+Driver+17+for+SQL+Server
```

### For PostgreSQL:
1. Install: `pip install psycopg2`
2. Update ONLY the `.env` file:
```
DATABASE_URL=postgresql://username:password@localhost:5432/assignment_db
```

**That's it! No code changes needed - SQLAlchemy handles everything!**

## Database Migrations (Optional)

For production, use Flask-Migrate to manage database schema changes:

```bash
# Initialize migrations
flask db init

# Create a migration
flask db migrate -m "Initial migration"

# Apply migrations
flask db upgrade
```

## Development Notes

- The API automatically creates or updates records based on the phone number
- Phone numbers are stored with the + prefix (e.g., +60123456789)
- If no assignee is provided in the webhook, the field will be set to null
- The application uses SQLAlchemy ORM for database portability between PostgreSQL and MS SQL Server