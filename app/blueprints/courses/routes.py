from flask import request, jsonify
from . import courses_bp
from .models import db, Course

@courses_bp.route('/', methods=['GET'])
def get_courses():
    courses = Course.query.all()
    return jsonify([course.name for course in courses])

@courses_bp.route('/', methods=['POST'])
def add_course():
    data = request.get_json()
    new_course = Course(
        course_name=data['course_name'],
        location=data['location'],
        number_of_holes=data['number_of_holes']
    )
    db.session.add(new_course)
    db.session.commit()
    return jsonify({'message': 'Course added successfully'}), 201
