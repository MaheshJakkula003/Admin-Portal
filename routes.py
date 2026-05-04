from flask import Blueprint, request, jsonify, render_template, current_app
from flask_login import login_user, login_required, current_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import URLSafeTimedSerializer
from models import db, Admin, Opportunity
from datetime import datetime
import re

routes = Blueprint('routes', __name__)

@routes.route('/')
def home():
    return render_template('admin.html')

@routes.route('/api/check-session')
@login_required
def check_session():
    return jsonify({
        "status": "success",
        "logged_in": True,
        "user": current_user.email
    }), 200

def is_valid_email(email):
    return re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", email)

@routes.route('/api/signup', methods=['POST'])
def signup():
    data = request.get_json() or {}

    full_name = data.get('full_name')
    email = data.get('email')
    password = data.get('password')
    confirm = data.get('confirm_password')

    if not all([full_name, email, password, confirm]):
        return jsonify({"error": "All fields required"}), 400

    if not is_valid_email(email):
        return jsonify({"error": "Invalid email format"}), 400

    if password != confirm:
        return jsonify({"error": "Passwords do not match"}), 400

    if len(password) < 8:
        return jsonify({"error": "Password must be at least 8 characters"}), 400

    if Admin.query.filter_by(email=email).first():
        return jsonify({"error": "Email already exists"}), 400

    hashed_pw = generate_password_hash(password)

    new_user = Admin(
        full_name=full_name,
        email=email,
        password_hash=hashed_pw
    )

    db.session.add(new_user)
    db.session.commit()

    return jsonify({
        "status": "success",
        "message": "Signup successful"
    }), 201

@routes.route('/api/login', methods=['POST'])
def login():
    data = request.get_json() or {}

    email = data.get('email')
    password = data.get('password')
    remember = data.get('remember', False) 

    user = Admin.query.filter_by(email=email).first()

    if not user or not check_password_hash(user.password_hash, password):
        return jsonify({"error": "Invalid email or password"}), 401

    login_user(user, remember=remember)

    return jsonify({
        "status": "success",
        "message": "Login successful",
        "user": {
            "id": user.id,
            "email": user.email
        }
    }), 200

@routes.route('/api/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    return jsonify({
        "status": "success",
        "message": "Logged out successfully"
    }), 200

@routes.route('/api/forgot-password', methods=['POST'])
def forgot_password():
    data = request.get_json() or {}
    email = data.get('email')

    user = Admin.query.filter_by(email=email).first()

    if user:
        serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
        token = serializer.dumps(user.email, salt='password-reset-salt')
        print(f"Reset link (expires in 1 hour): http://localhost:5000/reset/{token}")

    return jsonify({
        "status": "success",
        "message": "If email exists, reset link sent"
    }), 200

ALLOWED_CATEGORIES = [
    "Technology", "Business", "Design",
    "Marketing", "Data Science", "Other"
]

@routes.route('/api/opportunities', methods=['GET'])
@login_required
def get_opportunities():
    ops = Opportunity.query.filter_by(admin_id=current_user.id).all()

    return jsonify({
        "status": "success",
        "data": [op.to_dict() for op in ops]
    }), 200

@routes.route('/api/opportunities/<int:id>', methods=['GET'])
@login_required
def get_opportunity(id):
    op = Opportunity.query.get_or_404(id)

    if op.admin_id != current_user.id:
        return jsonify({"error": "Unauthorized"}), 403

    return jsonify({
        "status": "success",
        "data": op.to_dict()
    }), 200

@routes.route('/api/opportunities', methods=['POST'])
@login_required
def create_opportunity():
    data = request.get_json() or {}

    required_fields = ['title', 'duration', 'start_date', 'description', 'skills', 'category']

    for field in required_fields:
        if not data.get(field):
            return jsonify({"error": f"{field} is required"}), 400

    if data.get('category') not in ALLOWED_CATEGORIES:
        return jsonify({"error": "Invalid category"}), 400

    try:
        start_date = datetime.strptime(data['start_date'], "%Y-%m-%d").date()
        end_date = None

        if data.get('end_date'):
            end_date = datetime.strptime(data['end_date'], "%Y-%m-%d").date()

            if end_date < start_date:
                return jsonify({"error": "End date cannot be before start date"}), 400

    except:
        return jsonify({"error": "Invalid date format"}), 400

    try:
        max_applicants = int(data.get('max_applicants') or 0)
    except:
        return jsonify({"error": "max_applicants must be a number"}), 400

    op = Opportunity(
        title=data['title'],
        duration=data['duration'],
        start_date=start_date,
        end_date=end_date,
        description=data['description'],
        skills=data['skills'],
        category=data['category'],
        future_opportunities=data.get('future_opportunities'),
        max_applicants=max_applicants,
        admin_id=current_user.id
    )

    db.session.add(op)
    db.session.commit()

    return jsonify({
        "status": "success",
        "message": "Opportunity created successfully",
        "data": op.to_dict()
    }), 201

@routes.route('/api/opportunities/<int:id>', methods=['PUT'])
@login_required
def update_opportunity(id):
    op = Opportunity.query.get_or_404(id)

    if op.admin_id != current_user.id:
        return jsonify({"error": "Unauthorized"}), 403

    data = request.get_json() or {}

    try:
        if data.get('title'): op.title = data['title']
        if data.get('duration'): op.duration = data['duration']
        if data.get('description'): op.description = data['description']
        if data.get('skills'): op.skills = data['skills']
        if data.get('category'): op.category = data['category']
        if 'future_opportunities' in data: op.future_opportunities = data['future_opportunities']
        if 'max_applicants' in data: op.max_applicants = int(data['max_applicants'] or 0)

        if data.get('start_date'):
            op.start_date = datetime.strptime(data['start_date'], "%Y-%m-%d").date()
        
        if data.get('end_date'):
            op.end_date = datetime.strptime(data['end_date'], "%Y-%m-%d").date()
        elif 'end_date' in data: 
            op.end_date = None

        db.session.commit()
        return jsonify({
            "status": "success", 
            "message": "Opportunity updated successfully",
            "data": op.to_dict()
        }), 200

    except ValueError:
        return jsonify({"error": "Invalid data format"}), 400

@routes.route('/api/opportunities/<int:id>', methods=['DELETE'])
@login_required
def delete_opportunity(id):
    op = Opportunity.query.get_or_404(id)

    if op.admin_id != current_user.id:
        return jsonify({"error": "Unauthorized"}), 403

    db.session.delete(op)
    db.session.commit()

    return jsonify({
        "status": "success",
        "message": "Opportunity deleted successfully"
    }), 200