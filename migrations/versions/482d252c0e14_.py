"""empty message

Revision ID: 482d252c0e14
Revises: c0ae60a9fc17
Create Date: 2018-07-21 16:16:32.188578

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '482d252c0e14'
down_revision = 'c0ae60a9fc17'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('ih_order_info', sa.Column('trade_no', sa.String(length=128), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('ih_order_info', 'trade_no')
    # ### end Alembic commands ###
