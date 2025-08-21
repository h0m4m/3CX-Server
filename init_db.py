from app import app
from models import db, Assignment

def init_database():
    """Initialize the database with tables"""
    with app.app_context():
        # Create all tables
        db.create_all()
        print("Database tables created successfully!")
        
        # Optional: Add sample data
        sample_assignments = [
            Assignment(customer_phone='+60123456789', assignee='John Doe'),
            Assignment(customer_phone='+60198765432', assignee='Jane Smith'),
        ]
        
        for assignment in sample_assignments:
            existing = Assignment.query.filter_by(customer_phone=assignment.customer_phone).first()
            if not existing:
                db.session.add(assignment)
        
        try:
            db.session.commit()
            print("Sample data added successfully!")
        except Exception as e:
            print(f"Sample data might already exist: {e}")
            db.session.rollback()

if __name__ == '__main__':
    init_database()