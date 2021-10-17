"""empty message

Revision ID: ff81191d0d31
Revises: c86e2dc9e356
Create Date: 2021-10-18 02:07:55.491671

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ff81191d0d31'
down_revision = 'c86e2dc9e356'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('user', sa.Column('about_me', sa.VARCHAR(length=140), nullable=True))


def downgrade():
    op.drop_column('user', 'about_me')