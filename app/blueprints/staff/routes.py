from flask import request, jsonify, current_app
from . import staff_bp
from .models import db, Staff
from flask_jwt_extended import create_access_token

@staff_bp.route('/register', methods=['POST'])
def register_staff():
    data = request.get_json()
    # Assuming the frontend sends pin as 'pin' instead of misusing 'password' key
    new_staff = Staff(
        first_name=data['first_name'],
        last_name=data['last_name'],
        position=data['position'],
        email=data['email'],
        phone=data['phone'],
        pin=data['pin'],  # Directly use 'pin' here
        club_id=data['club_id']
    )
    db.session.add(new_staff)
    db.session.commit()
    return jsonify({"message": "Staff registered successfully"}), 201

@staff_bp.route('/fixedlogin', methods=['POST'])
def authenticate_staff():
    data = request.get_json()
    if not data or 'email' not in data or 'pin' not in data:
        return jsonify({"msg": "Missing email or pin in request"}), 400

    staff = Staff.query.filter_by(email=data['email']).first()
    if staff and staff.verify_pin(data['pin']):
        access_token = create_access_token(identity={'email': staff.email, 'role': 'staff'})
        return jsonify({
            "access_token": access_token, 
            "staff_id": staff.id, 
            "club_id": staff.club_id,
            "isStaff": True  
        }), 200
    else:
        return jsonify({"msg": "Invalid email or pin"}), 401