"""modification type added to sentence

Revision ID: 104e69813dd6
Revises: 284415c9d550
Create Date: 2019-12-03 16:43:39.220268

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '104e69813dd6'
down_revision = '284415c9d550'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('sentence', schema=None) as batch_op:
        batch_op.add_column(sa.Column('modification', sa.Enum('HEDG', 'AHEDG', 'NEG', 'HIPER', 'HIPO', 'SYN', name='modificationtypes'), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('sentence', schema=None) as batch_op:
        batch_op.drop_column('modification')

    # ### end Alembic commands ###
