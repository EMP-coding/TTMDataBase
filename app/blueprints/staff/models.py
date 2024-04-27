from ...extensions import db  
from ...blueprints.courses.models import Club

class Staff(db.Model):
    __tablename__ = 'staff'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(255))
    last_name = db.Column(db.String(255))
    position = db.Column(db.String(255))
    email = db.Column(db.String(255), unique=True)
    phone = db.Column(db.String(20))
    pin = db.Column(db.String(4))  
    club_id = db.Column(db.Integer, db.ForeignKey('club.id'), nullable=False)
    club = db.relationship('Club', back_populates='staff')


    def verify_pin(self, pin):
        """Verify the pin directly without hashing."""
        return self.pin == pin
