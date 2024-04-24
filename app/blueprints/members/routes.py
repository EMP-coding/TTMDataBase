from flask import request, jsonify
from . import members_bp
from .models import db, Member
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token

from flask import request, jsonify
from . import members_bp
from .models import db, Member
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token

@members_bp.route('/all', methods=['GET'])
def get_members():
    members = Member.query.all()
    return jsonify({'members': [member.first_name for member in members]})

@members_bp.route('/create', methods=['POST'])
def add_member():
    data = request.json
    new_member = Member(
        first_name=data['first_name'], 
        last_name=data['last_name'],
        email=data['email'],
        phone=data['phone'],
        address=data['address'],
        membership_type=data['membership_type'],
        password=generate_password_hash(data['password'])
    )
    db.session.add(new_member)
    db.session.commit()
    return jsonify({'message': 'Member added successfully'}), 201

@members_bp.route('/register', methods=['POST'])
def register_member():
    data = request.get_json()

    # Define required fields
    required_fields = ['first_name', 'last_name', 'email', 'password']

    # Create a new Member instance with required fields
    new_member_data = {field: data[field] for field in required_fields}

    # Add optional fields with default value None if not present
    optional_fields = ['phone', 'address', 'membership_type']
    for field in optional_fields:
        new_member_data[field] = data.get(field, None)

    # Create a new Member instance with the validated data
    new_member = Member(**new_member_data)

    db.session.add(new_member)
    db.session.commit()

    return jsonify({"message": "Member registered successfully"}), 201




@members_bp.route('/login', methods=['POST'])
def authenticate_member():
    data = request.get_json()
    member = Member.query.filter_by(email=data['email']).first()
    if member and check_password_hash(member.password_hash, data['password']):
        access_token = create_access_token(identity={'email': member.email, 'role': 'member'})
        return jsonify(access_token=access_token), 200
    return jsonify({"msg": "Invalid credentials"}), 401