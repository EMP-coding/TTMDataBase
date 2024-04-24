from ...extensions import db  # Adjust this import based on your project's structure
from werkzeug.security import generate_password_hash, check_password_hash
from ...blueprints.courses.models import Club

class Staff(db.Model):
    __tablename__ = 'staff'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(255))
    last_name = db.Column(db.String(255))
    position = db.Column(db.String(255))
    email = db.Column(db.String(255), unique=True)
    phone = db.Column(db.String(20))
    password_hash = db.Column(db.String(128))
    club_id = db.Column(db.Integer, db.ForeignKey('club.id'), nullable=False)
    club = db.relationship('Club', back_populates='staff')

    @property
    def password(self):
        raise AttributeError('password is not readable')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)