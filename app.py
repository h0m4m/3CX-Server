from flask import Flask, request, jsonify
from flask_migrate import Migrate
from models import db, Assignment
from config import Config
import logging
import os

# Map incoming assignee names to specific ID numbers
ASSIGNEE_TO_ID = {
    "Mahmoud Dana": 269,
    "Farouk Elewi": 291,
    "Jessica Espanola": 110,
    "Sajjad Rehman": 272,
    "Mansour -": 270,
    "Noor Barakat": 271,
    "Mohamed Al Nour": 806,
    "Adnan fayed": 806,
}

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Initialize database
    db.init_app(app)
    
    # Initialize Flask-Migrate
    migrate = Migrate(app, db)
    
    return app

app = create_app()

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy'}), 200

@app.route('/webhook/contact', methods=['POST'])
def contact_webhook():
    """
    Webhook endpoint to handle contact assignment updates
    Expected payload format:
    {
        "contact": {
            "phone": "+60123456789",
            "assignee": {
                "firstName": "John",
                "lastName": "Doe"
            }
        },
        "event_type": "contact.assignee.updated"
    }
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No JSON data provided'}), 400
        
        logger.info(f"Received webhook: {data.get('event_type', 'unknown')}")
        
        # Extract relevant data from webhook
        contact = data.get('contact', {})
        phone = contact.get('phone')
        
        if not phone:
            return jsonify({'error': 'Phone number is required'}), 400
        
        # Extract assignee name
        assignee_info = contact.get('assignee', {})
        assignee_name = None
        assignee_mapped_id = None
        
        if assignee_info:
            first_name = assignee_info.get('firstName', '')
            last_name = assignee_info.get('lastName', '')
            if first_name or last_name:
                assignee_name = f"{first_name} {last_name}".strip()
                # Map the full name to an ID if available
                assignee_mapped_id = ASSIGNEE_TO_ID.get(assignee_name)
        
        # Check if assignment exists
        assignment = Assignment.query.filter_by(customer_phone=phone).first()
        
        if assignment:
            # Update existing assignment
            # Store mapped ID if found, otherwise store the name
            assignment.assignee = str(assignee_mapped_id) if assignee_mapped_id is not None else assignee_name
            logger.info(f"Updated assignment for {phone}: {assignee_name}")
            action = 'updated'
        else:
            # Create new assignment
            assignment = Assignment(
                customer_phone=phone,
                # Store mapped ID if found, otherwise store the name
                assignee=(str(assignee_mapped_id) if assignee_mapped_id is not None else assignee_name)
            )
            db.session.add(assignment)
            logger.info(f"Created new assignment for {phone}: {assignee_name}")
            action = 'created'
        
        # Commit the changes
        db.session.commit()
        
        return jsonify({
            'status': 'success',
            'action': action,
            'assignment': assignment.to_dict()
        }), 200
        
    except Exception as e:
        logger.error(f"Error processing webhook: {str(e)}")
        db.session.rollback()
        return jsonify({'error': 'Internal server error', 'message': str(e)}), 500

@app.route('/assignments', methods=['GET'])
def get_assignments():
    """Get all assignments"""
    try:
        assignments = Assignment.query.all()
        return jsonify({
            'assignments': [a.to_dict() for a in assignments],
            'count': len(assignments)
        }), 200
    except Exception as e:
        logger.error(f"Error fetching assignments: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/assignments/<phone>', methods=['GET'])
def get_assignment_by_phone(phone):
    """Get assignment by phone number"""
    try:
        # Add + if not present
        if not phone.startswith('+'):
            phone = '+' + phone
            
        assignment = Assignment.query.filter_by(customer_phone=phone).first()
        
        if not assignment:
            return jsonify({'error': 'Assignment not found'}), 404
        
        return jsonify(assignment.to_dict()), 200
    except Exception as e:
        logger.error(f"Error fetching assignment: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    # Use PORT environment variable if set, otherwise default to 8000
    port = int(os.environ.get('PORT', 8000))
    app.run(debug=True, host='0.0.0.0', port=port)
