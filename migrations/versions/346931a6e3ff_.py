"""empty message

Revision ID: 346931a6e3ff
Revises: 
Create Date: 2019-03-28 02:01:16.663316

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '346931a6e3ff'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('driver',
    sa.Column('id', sa.String(length=40), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('born_date', sa.Date(), nullable=False),
    sa.Column('gender', sa.Integer(), nullable=False),
    sa.Column('has_truck', sa.Boolean(), nullable=False),
    sa.Column('is_loaded', sa.Boolean(), nullable=False),
    sa.Column('created_date', sa.DateTime(), nullable=False),
    sa.Column('cnh_type', sa.String(length=5), nullable=False),
    sa.Column('truck_type', sa.Integer(), nullable=False),
    sa.Column('lat_origin', sa.String(length=15), nullable=False),
    sa.Column('lng_origin', sa.String(length=15), nullable=False),
    sa.Column('lat_destination', sa.String(length=15), nullable=False),
    sa.Column('lng_destination', sa.String(length=15), nullable=False),
    sa.Column('is_removed', sa.Boolean(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('driver')
    # ### end Alembic commands ###
