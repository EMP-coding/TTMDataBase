from ...extensions import db  # Adjust this import based on your project's structure
from werkzeug.security import generate_password_hash, check_password_hash


class Member(db.Model):
    __tablename__ = 'member'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(255))
    last_name = db.Column(db.String(255))
    email = db.Column(db.String(255), unique=True)
    phone = db.Column(db.String(20))
    address = db.Column(db.Text)
    membership_type = db.Column(db.String(100))
    password_hash = db.Column(db.String(255))
    bookings = db.relationship('Booking', backref='member', lazy=True)

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)