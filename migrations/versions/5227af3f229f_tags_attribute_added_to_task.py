"""tags attribute added to Task

Revision ID: 5227af3f229f
Revises: 9f135cd1d24f
Create Date: 2019-11-08 13:13:45.915713

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5227af3f229f'
down_revision = '9f135cd1d24f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('task', schema=None) as batch_op:
        batch_op.add_column(sa.Column('tags', sa.String(length=200), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('task', schema=None) as batch_op:
        batch_op.drop_column('tags')

    # ### end Alembic commands ###