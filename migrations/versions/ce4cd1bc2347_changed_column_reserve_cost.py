"""Changed_column_reserve_cost

Revision ID: ce4cd1bc2347
Revises: a3a7621188df
Create Date: 2021-11-11 17:13:29.864979

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'ce4cd1bc2347'
down_revision = 'a3a7621188df'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('reserve', 'reserve_cost',
               existing_type=mysql.INTEGER(),
               nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('reserve', 'reserve_cost',
               existing_type=mysql.INTEGER(),
               nullable=False)
    # ### end Alembic commands ###
