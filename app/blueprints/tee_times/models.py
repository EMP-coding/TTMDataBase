from ...extensions import db
from datetime import datetime
import enum

class TeeTime(db.Model):
    __tablename__ = 'tee_time'
    id = db.Column(db.Integer, primary_key=True)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'))
    available = db.Column(db.Boolean, default=True)
    bookings = db.relationship('Booking', backref='tee_time', lazy=True)

class BookingStatus(enum.Enum): # Creating 
    booked = "Booked"
    cancelled = "Cancelled"
    confirmed = "Confirmed"

class Booking(db.Model):
    __tablename__ = 'booking'
    status = db.Column(db.Enum(BookingStatus), default=BookingStatus.booked, nullable=False) # Creating a status column using enum to allow 3 states 
    id = db.Column(db.Integer, primary_key=True)
    member_id = db.Column(db.Integer, db.ForeignKey('member.id'))
    tee_time_id = db.Column(db.Integer, db.ForeignKey('tee_time.id'))
    booked_at = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(50), nullable=False, default='Booked')