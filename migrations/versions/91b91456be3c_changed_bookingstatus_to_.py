"""changed BookingStatus to BookingStatusTwo

Revision ID: 91b91456be3c
Revises: 79fdf6e4f4ed
Create Date: 2024-05-06 20:37:55.658616

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '91b91456be3c'
down_revision = '79fdf6e4f4ed'
branch_labels = None
depends_on = None


def upgrade():
    # Assuming 'bookingstatustwo' is the new enum type's name in PostgreSQL
    booking_status_two = sa.Enum('booked', 'cancelled', 'checked in', name='bookingstatustwo')
    booking_status_two.create(op.get_bind(), checkfirst=True)
    
    # Explicitly specifying the casting process
    op.execute(
        """
        ALTER TABLE booking 
        ALTER COLUMN status TYPE bookingstatustwo USING status::text::bookingstatustwo;
        """
    )

def downgrade():
    # Revert to the old enum type and possibly delete the new enum if needed
    op.execute(
        """
        ALTER TABLE booking 
        ALTER COLUMN status TYPE bookingstatus USING status::text::bookingstatus;
        """
    )
    booking_status_two = sa.Enum('booked', 'cancelled', 'checked in', name='bookingstatustwo')
    booking_status_two.drop(op.get_bind(), checkfirst=True)