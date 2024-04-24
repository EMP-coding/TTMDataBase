from flask import request, jsonify
from . import tee_times_bp
from .models import db, TeeTime, Booking, BookingStatus
from datetime import datetime, timedelta
from flask_jwt_extended import jwt_required, get_jwt_identity

@tee_times_bp.route('/generate', methods=['POST'])
def generate_tee_times():
    data = request.json
    course_id = data['course_id']
    start_time = datetime.strptime(data['start_time'], '%Y-%m-%d %H:%M')
    end_time = datetime.strptime(data['end_time'], '%Y-%m-%d %H:%M')
    interval_minutes = data.get('interval_minutes', 10)
    current_time = start_time
    while current_time < end_time:
        tee_time = TeeTime(
            start_time=current_time,
            end_time=current_time + timedelta(minutes=interval_minutes),
            course_id=course_id,
            available=True
        )
        db.session.add(tee_time)
        current_time += timedelta(minutes=interval_minutes)
    db.session.commit()
    return jsonify({'message': 'Tee times generated successfully'}), 201

@tee_times_bp.route('/all', methods=['GET'])  # Added the missing slash (/) in the route path
def get_tee_times():
    tee_times = TeeTime.query.all()
    tee_times_list = [{
        'id': tee.id,
        'start_time': tee.start_time.isoformat(),
        'end_time': tee.end_time.isoformat(),
        'course_id': tee.course_id,
        'available': tee.available
    } for tee in tee_times]
    return jsonify(tee_times_list)

# Updated the route definition to use tee_times_bp instead of app
@tee_times_bp.route('/bookings/<int:booking_id>', methods=['PUT'])
def update_booking(booking_id):
    data = request.get_json()
    booking = Booking.query.get(booking_id)
    if not booking:
        return jsonify({'error': 'Booking not found'}), 404

    try:
        booking.status = BookingStatus[data['status']]
        db.session.commit()
        return jsonify({'message': 'Booking status updated successfully'}), 200
    except KeyError:
        return jsonify({'error': 'Invalid status provided'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500
