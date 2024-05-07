from flask import request, jsonify
from . import course_bp
from .models import db, Course
# Need to adjust below route to include all data. 
@course_bp.route('/all', methods=['GET'])
def get_courses():
    courses = Course.query.all()
    return jsonify([course.name for course in courses])


# Route to get courses by club_id
@course_bp.route('/<int:club_id>', methods=['GET'])
def get_courses_by_club_id(club_id):
    
    courses = Course.query.filter_by(club_id=club_id).all()

    
    course_list = [{
        'id': course.id,
        'course_name': course.course_name,
        'location': course.location,
        'number_of_holes': course.number_of_holes
    } for course in courses]

    
    return jsonify(course_list)

@course_bp.route('/new', methods=['POST'])
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
