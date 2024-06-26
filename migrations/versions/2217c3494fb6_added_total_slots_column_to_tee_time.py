"""added total_slots column to tee_time

Revision ID: 2217c3494fb6
Revises: 64f1b0f83faf
Create Date: 2024-04-24 20:28:21.166677

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2217c3494fb6'
down_revision = '64f1b0f83faf'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('tee_time', schema=None) as batch_op:
        batch_op.add_column(sa.Column('total_slots', sa.Integer(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('tee_time', schema=None) as batch_op:
        batch_op.drop_column('total_slots')

    # ### end Alembic commands ###
