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

    def has_available_slots(self, players_to_reserve):
        available_slots = self.total_slots - self.booking_count()
        return available_slots >= players_to_reserve

    def booking_count(self):
        return len(self.bookings)

    def is_available(self):
        return len(self.bookings) < self.total_slots

    def booking_count(self):
        return len(self.bookings)

class BookingStatusTwo(enum.Enum):
    BOOKED = "BOOKED"
    CANCELLED = "CANCELLED"
    CHECKED_IN = "CHECKED_IN"

class Booking(db.Model):
    __tablename__ = 'booking'
    id = db.Column(db.Integer, primary_key=True)
    member_id = db.Column(db.Integer, db.ForeignKey('member.id'))
    tee_time_id = db.Column(db.Integer, db.ForeignKey('tee_time.id'))
    status = db.Column(db.Enum(BookingStatusTwo), default=BookingStatusTwo.BOOKED, nullable=False)
    booked_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    payment_status = db.Column(db.String(50))  # 'Pending', 'Completed', 'Refunded'
    amount_paid = db.Column(db.Numeric(10, 2))  

    def __repr__(self):
        return f'<Booking {self.id} - Status: {self.status}>'
    

