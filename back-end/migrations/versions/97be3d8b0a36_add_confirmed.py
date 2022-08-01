"""add confirmed

Revision ID: 97be3d8b0a36
Revises: fa29e0671808
Create Date: 2022-08-01 10:13:24.216614

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '97be3d8b0a36'
down_revision = 'fa29e0671808'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('confirmed', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'confirmed')
    # ### end Alembic commands ###