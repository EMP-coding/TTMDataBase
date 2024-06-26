"""Adjusted TeeTime Column

Revision ID: 64f1b0f83faf
Revises: efd6c1daa92c
Create Date: 2024-04-24 20:03:13.474355

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '64f1b0f83faf'
down_revision = 'efd6c1daa92c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('booking', schema=None) as batch_op:
        batch_op.alter_column('status',
               existing_type=sa.VARCHAR(length=50),
               type_=sa.Enum('booked', 'cancelled', 'confirmed', name='bookingstatus'),
               existing_nullable=False)

    with op.batch_alter_table('tee_time', schema=None) as batch_op:
        batch_op.drop_column('available')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('tee_time', schema=None) as batch_op:
        batch_op.add_column(sa.Column('available', sa.BOOLEAN(), autoincrement=False, nullable=True))

    with op.batch_alter_table('booking', schema=None) as batch_op:
        batch_op.alter_column('status',
               existing_type=sa.Enum('booked', 'cancelled', 'confirmed', name='bookingstatus'),
               type_=sa.VARCHAR(length=50),
               existing_nullable=False)

    # ### end Alembic commands ###
