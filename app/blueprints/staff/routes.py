from flask import request, jsonify
from . import staff_bp
from .models import db, Staff
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token

@staff_bp.route('/register', methods=['POST'])
def register_staff():
    data = request.get_json()
    new_staff = Staff(
        first_name=data['first_name'],
        last_name=data['last_name'],
        position=data['position'],
        email=data['email'],
        phone=data['phone'],
        password=generate_password_hash(data['password'])
    )
    db.session.add(new_staff)
    db.session.commit()
    return jsonify({"message": "Staff registered successfully"}), 201

@staff_bp.route('/login', methods=['POST'])
def authenticate_staff():
    data = request.get_json()
    staff = Staff.query.filter_by(email=data['email']).first()
    if staff and check_password_hash(staff.password_hash, data['password']):
        access_token = create_access_token(identity={'email': staff.email, 'role': 'staff'})
        return jsonify(access_token=access_token), 200
    return jsonify({"msg": "Invalid credentials"}), 401


