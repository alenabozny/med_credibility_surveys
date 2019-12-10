"""empty message

Revision ID: 6b63667105e1
Revises: 104e69813dd6
Create Date: 2019-12-10 22:02:51.335045

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6b63667105e1'
down_revision = '104e69813dd6'
branch_labels = None
depends_on = None


def upgrade():
    op.alter_column('sentence', 'modification', existing_type=sa.Enum(), type_=sa.String(20))


def downgrade():
    op.alter_column('sentence', 'modification', existing_type=sa.String(20), type_=sa.Enum())
