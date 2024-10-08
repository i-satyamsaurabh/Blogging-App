"""Add likes column to Post db

Revision ID: 242c426f69b2
Revises: 
Create Date: 2024-09-11 12:36:07.810289

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '242c426f69b2'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('database', schema=None) as batch_op:
        batch_op.add_column(sa.Column('likes', sa.Integer(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('database', schema=None) as batch_op:
        batch_op.drop_column('likes')

    # ### end Alembic commands ###
