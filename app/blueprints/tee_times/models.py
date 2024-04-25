from ...extensions import db
from datetime import datetime
import enum

class TeeTime(db.Model):
    __tablename__ = 'tee_time'
    id = db.Column(db.Integer, primary_key=True)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'))
    total_slots = db.Column(db.Integer, nullable=False, default=4)  
    bookings = db.relationship('Booking', backref='tee_time', lazy=True)

    def is_available(self):
        return len(self.bookings) < self.total_slots

    def booking_count(self):
        return len(self.bookings)

class BookingStatus(enum.Enum):
    booked = "Booked"
    cancelled = "Cancelled"
    confirmed = "Confirmed"

class Booking(db.Model):
    __tablename__ = 'booking'
    status = db.Column(db.Enum(BookingStatus), default=BookingStatus.booked, nullable=False)
    id = db.Column(db.Integer, primary_key=True)
    member_id = db.Column(db.Integer, db.ForeignKey('member.id'))
    tee_time_id = db.Column(db.Integer, db.ForeignKey('tee_time.id'))
    booked_at = db.Column(db.DateTime, default=datetime.utcnow)
