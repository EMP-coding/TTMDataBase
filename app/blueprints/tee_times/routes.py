from flask import request, jsonify
from . import tee_times_bp
from .models import db, TeeTime, Booking, BookingStatusTwo
from datetime import datetime, timedelta, date
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..course.models import Course
from sqlalchemy.sql import func 
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
import enum



# Route to generate Tee Times
@tee_times_bp.route('/generate', methods=['POST'])
def generate_tee_times():
    data = request.json
    try:
        course_id = data['course_id']
        start_time = datetime.strptime(data['start_time'], '%Y-%m-%d %H:%M')
        end_time = datetime.strptime(data['end_time'], '%Y-%m-%d %H:%M')
        interval_minutes = data.get('interval_minutes', 10)
        
        current_time = start_time
        while current_time < end_time:
            tee_time = TeeTime(
                start_time=current_time,
                end_time=current_time + timedelta(minutes=interval_minutes),
                course_id=course_id
            )
            db.session.add(tee_time)
            current_time += timedelta(minutes=interval_minutes)
        
        db.session.commit()
        return jsonify({'message': 'Tee times generated successfully'}), 201
    except KeyError as e:
        return jsonify({'error': f'Missing required parameter: {str(e)}'}), 400
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'error': 'Database error'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Route to get all Tee Times
@tee_times_bp.route('/all', methods=['GET'])  
def get_tee_times():
    tee_times = TeeTime.query.all()
    tee_times_list = [{
        'id': tee.id,
        'start_time': tee.start_time.isoformat(),
        'end_time': tee.end_time.isoformat(),
        'course_id': tee.course_id,
    } for tee in tee_times]
    return jsonify(tee_times_list)

# Route to get available Tee Times
@tee_times_bp.route('/available', methods=['GET'])
def get_available_tee_times():
    course_id = request.args.get('course_id', type=int)
    date_str = request.args.get('date')
    if not course_id or not date_str:
        return jsonify({'error': 'course_id and date are required'}), 400

    try:
        
        date = datetime.strptime(date_str, '%Y-%m-%d')
    except ValueError:
        return jsonify({'error': 'invalid date format'}), 400

    # Calculate the end of the day for the date filter
    day_end = date + timedelta(days=1)

    subq = db.session.query(
        Booking.tee_time_id,
        func.count('*').label('booking_count')
    ).group_by(Booking.tee_time_id).subquery()

    available_tee_times = db.session.query(
        TeeTime.id,
        TeeTime.start_time,
        TeeTime.end_time,
        Course.course_name.label("course_name"),
        TeeTime.total_slots,
        (TeeTime.total_slots - func.coalesce(subq.c.booking_count, 0)).label('available_slots')
    ).outerjoin(subq, TeeTime.id == subq.c.tee_time_id)\
    .join(Course)\
    .filter(TeeTime.course_id == course_id)\
    .filter(TeeTime.start_time >= date, TeeTime.start_time < day_end)\
    .filter(TeeTime.total_slots > func.coalesce(subq.c.booking_count, 0))\
    .all()

    available_tee_times_list = [{
        'id': tee.id,
        'start_time': tee.start_time.isoformat(),
        'end_time': tee.end_time.isoformat(),
        'course_name': tee.course_name,
        'available_slots': tee.available_slots,
        'total_slots': tee.total_slots
    } for tee in available_tee_times]

    return jsonify(available_tee_times_list)

# Route to update a booking
@tee_times_bp.route('/bookings/<int:booking_id>', methods=['PUT'])
def update_booking(booking_id):
    data = request.get_json()
    booking = Booking.query.get(booking_id)
    if not booking:
        return jsonify({'error': 'Booking not found'}), 404

    try:
        booking.status = BookingStatusTwo[data['status']]
        db.session.commit()
        return jsonify({'message': 'Booking status updated successfully'}), 200
    except KeyError:
        return jsonify({'error': 'Invalid status provided'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Route to reserve Tee Time
@tee_times_bp.route('/reserve', methods=['POST'])
def reserve_tee_time():
    member_id = request.json.get('member_id')
    tee_time_id = request.json.get('tee_time_id')
    players_to_reserve = request.json.get('players')  # New parameter to specify the number of players

    # Fetch the tee time
    tee_time = TeeTime.query.get(tee_time_id)
    if not tee_time:
        return jsonify({'error': 'Tee time not found'}), 404

    # Check availability
    if not tee_time.has_available_slots(players_to_reserve):  # Check availability for the specified number of players
        return jsonify({'error': 'Not enough available slots for the specified number of players'}), 400

    # Create bookings for each player
    bookings = []
    for _ in range(players_to_reserve):
        booking = Booking(
            member_id=member_id,
            tee_time_id=tee_time_id,
            status=BookingStatusTwo.BOOKED,
            booked_at=datetime.utcnow()
        )
        bookings.append(booking)

    
    db.session.add_all(bookings)
    try:
        db.session.commit()
        return jsonify({'message': 'Booking successful', 'booking_ids': [booking.id for booking in bookings]}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# Route to get bookings by member ID

@tee_times_bp.route('/bookings/member/<int:member_id>', methods=['GET'])
def get_bookings_by_member_id(member_id):
    try:
        bookings = Booking.query.filter_by(member_id=member_id).join(TeeTime).all()
        if not bookings:
            return jsonify({'message': 'No bookings found for this member.'}), 404

        booking_details = [{
            'id': booking.id,
            'tee_time_id': booking.tee_time_id,
            'booked_at': booking.booked_at.isoformat(),
            'status': booking.status.value,
            'tee_time_start': booking.tee_time.start_time.isoformat(),
            'tee_time_end': booking.tee_time.end_time.isoformat(),
            'course_name': booking.tee_time.course.course_name
        } for booking in bookings]

        return jsonify(booking_details)
    except SQLAlchemyError as e:
        return jsonify({'error': 'Database error', 'details': str(e)}), 500
    except Exception as e:
        return jsonify({'error': 'Internal server error', 'details': str(e)}), 500
    

# Route to delete bookings for a member and tee time
@tee_times_bp.route('/<int:tee_time_id>/member/<int:member_id>', methods=['DELETE'])
def delete_member_bookings(tee_time_id, member_id):
    try:
        # Delete bookings for the specified member and tee time
        result = Booking.query.filter_by(tee_time_id=tee_time_id, member_id=member_id).delete()
        db.session.commit()

        if result > 0:
            return jsonify({'message': f'Successfully deleted {result} bookings for member {member_id}.'}), 200
        else:
            return jsonify({'message': 'No bookings found for this member and tee time.'}), 404

    except SQLAlchemyError as e:
        db.session.rollback()  
        return jsonify({'error': 'Database error', 'details': str(e)}), 500
    except Exception as e:
        db.session.rollback()  
        return jsonify({'error': 'Internal server error', 'details': str(e)}), 500

# Route to get bookings by tee time for a selected date
@tee_times_bp.route('/bookings', methods=['GET'])
def get_bookings_by_tee_time():
    selected_date_str = request.args.get('date')
    if not selected_date_str:
        return jsonify({'error': 'Date parameter is required.'}), 400

    try:
        selected_date = datetime.strptime(selected_date_str, '%Y-%m-%d').date()
    except ValueError:
        return jsonify({'error': 'Invalid date format. Please use YYYY-MM-DD format.'}), 400

    tee_times = TeeTime.query.filter(
        func.date(TeeTime.start_time) == selected_date
    ).all()

    tee_times_with_bookings = []
    for tee_time in tee_times:
        tee_time_dict = {
            'id': tee_time.id,
            'start_time': tee_time.start_time.isoformat(),
            'end_time': tee_time.end_time.isoformat(),
            'course_id': tee_time.course_id,
            'bookings': []  # Initialize an empty list to store bookings
        }
        for booking in tee_time.bookings:
            booking_data = {
                'booking_id': booking.id,
                'member_id': booking.member_id,
                'status': booking.status.value,  
                'booked_at': booking.booked_at.isoformat()
            }
            tee_time_dict['bookings'].append(booking_data)  
        tee_times_with_bookings.append(tee_time_dict)

    return jsonify(tee_times_with_bookings)