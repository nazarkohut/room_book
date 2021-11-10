"""Changed_city_data

Revision ID: 8e2d4102f277
Revises: 999dd83c6560
Create Date: 2021-11-10 23:00:38.877287

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '8e2d4102f277'
down_revision = '999dd83c6560'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('city', sa.Column('city', sa.String(length=50), nullable=False))
    op.drop_column('city', 'city_name')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('city', sa.Column('city_name', mysql.VARCHAR(length=50), nullable=False))
    op.drop_column('city', 'city')
    # ### end Alembic commands ###
