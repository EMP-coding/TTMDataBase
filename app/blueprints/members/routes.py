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

    
    required_fields = ['first_name', 'last_name', 'email', 'password']

    
    new_member_data = {field: data[field] for field in required_fields}

    
    optional_fields = ['phone', 'address', 'membership_type']
    for field in optional_fields:
        new_member_data[field] = data.get(field, None)

    
    new_member = Member(**new_member_data)

    db.session.add(new_member)
    db.session.commit()

    return jsonify({"message": "Member registered successfully"}), 201




@members_bp.route('/login', methods=['POST'])
def authenticate_member():
    data = request.get_json()
    # Ensure the member query includes the club_id by joining with the Club table if necessary
    member = Member.query.filter_by(email=data['email']).first()
    if member and check_password_hash(member.password_hash, data['password']):
        access_token = create_access_token(identity={'email': member.email, 'role': 'member', 'club_id': member.club_id})
        # Include member_id and club_id in the response
        return jsonify(access_token=access_token, member_id=member.id, club_id=member.club_id), 200
    return jsonify({"msg": "Invalid credentials"}), 401

# Route to get member by id 
@members_bp.route('/m/<int:member_id>', methods=['GET'])
def get_member_by_id(member_id):
    member = Member.query.get(member_id)
    if not member:
        return jsonify({'message': 'Member not found'}), 404
    member_data = {
        'id': member.id,
        'first_name': member.first_name,
        'last_name': member.last_name,
        'email': member.email,
        'phone': member.phone,
        'address': member.address,
        'membership_type': member.membership_type
    }
    return jsonify(member_data), 200

# Route to update a member by id 

@members_bp.route('/update/<int:member_id>', methods=['PUT'])
def update_member(member_id):
    member = Member.query.get(member_id)
    if not member:
        return jsonify({'error': 'Member not found'}), 404
    
    data = request.get_json()
    try:
        member.first_name = data.get('first_name', member.first_name)
        member.last_name = data.get('last_name', member.last_name)
        member.email = data.get('email', member.email)
        member.phone = data.get('phone', member.phone)
        member.address = data.get('address', member.address)
        member.membership_type = data.get('membership_type', member.membership_type)
        
        db.session.commit()
        return jsonify({'message': 'Member updated successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500