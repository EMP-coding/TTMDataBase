"""empty message

Revision ID: 96fe6a3341f6
Revises: 654a02c1e93f
Create Date: 2024-04-23 18:59:04.423462

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '96fe6a3341f6'
down_revision = '654a02c1e93f'
branch_labels = None
depends_on = None


def upgrade():
    # Add the new column with the desired length
    op.alter_column('member', 'password_hash', type_=sa.String(255))

    with op.batch_alter_table('staff', schema=None) as batch_op:
        batch_op.add_column(sa.Column('club_id', sa.Integer(), nullable=False))
        batch_op.create_foreign_key(None, 'club', ['club_id'], ['id'])

    # ### end Alembic commands ###


def downgrade():
    # Revert the changes made in the upgrade function
    op.alter_column('member', 'password_hash', type_=sa.String(128))

    with op.batch_alter_table('staff', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_column('club_id')

    # ### end Alembic commands ###
