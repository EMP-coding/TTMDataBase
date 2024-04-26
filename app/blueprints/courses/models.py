from ...extensions import db  

class Course(db.Model):
    __tablename__ = 'course'
    id = db.Column(db.Integer, primary_key=True)
    course_name = db.Column(db.String(255))
    location = db.Column(db.Text)
    number_of_holes = db.Column(db.Integer)
    club_id = db.Column(db.Integer, db.ForeignKey('club.id'))
    tee_times = db.relationship('TeeTime', backref='course', lazy=True)

class Club(db.Model):
    __tablename__ = 'club'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(100), nullable=False)
    courses = db.relationship('Course', backref='club', lazy=True)
    staff = db.relationship('Staff', back_populates='club')