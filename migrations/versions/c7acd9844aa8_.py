"""empty message

Revision ID: c7acd9844aa8
Revises: 27926b790456
Create Date: 2019-11-01 23:46:56.350685

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c7acd9844aa8'
down_revision = '27926b790456'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_column('is_active')
        batch_op.drop_column('is_authenticated')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('is_authenticated', sa.BOOLEAN(), nullable=True))
        batch_op.add_column(sa.Column('is_active', sa.BOOLEAN(), nullable=True))

    # ### end Alembic commands ###
