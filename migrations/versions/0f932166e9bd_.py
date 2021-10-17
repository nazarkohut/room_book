"""empty message

Revision ID: 0f932166e9bd
Revises: ff81191d0d31
Create Date: 2021-10-18 02:08:32.968466

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0f932166e9bd'
down_revision = 'ff81191d0d31'
branch_labels = None
depends_on = None


def upgrade():
    op.alter_column('user', 'about_me', existing_type=sa.Integer(), type_=sa.BigInteger())


def downgrade():
    op.alter_column('user', 'about_me', existing_type=sa.BigInteger(), type_=sa.Integer())
