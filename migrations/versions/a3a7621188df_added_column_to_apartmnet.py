"""Added_column_to_apartmnet

Revision ID: a3a7621188df
Revises: 7b8f459a61b0
Create Date: 2021-11-11 15:57:28.863468

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a3a7621188df'
down_revision = '7b8f459a61b0'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('apartment', sa.Column('is_available', sa.Boolean(), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('apartment', 'is_available')
    # ### end Alembic commands ###
