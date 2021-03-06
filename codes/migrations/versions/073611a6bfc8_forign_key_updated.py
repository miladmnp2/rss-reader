"""Forign key updated

Revision ID: 073611a6bfc8
Revises: 7af6d217521a
Create Date: 2022-05-30 10:40:08.239757

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '073611a6bfc8'
down_revision = '7af6d217521a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('subscribers', sa.Column('publisher_id', sa.Integer(), nullable=False))
    op.drop_constraint('subscribers_feed_id_fkey', 'subscribers', type_='foreignkey')
    op.create_foreign_key(None, 'subscribers', 'publishers', ['publisher_id'], ['id'])
    op.drop_column('subscribers', 'feed_id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('subscribers', sa.Column('feed_id', sa.INTEGER(), autoincrement=False, nullable=False))
    op.drop_constraint(None, 'subscribers', type_='foreignkey')
    op.create_foreign_key('subscribers_feed_id_fkey', 'subscribers', 'feeds', ['feed_id'], ['id'])
    op.drop_column('subscribers', 'publisher_id')
    # ### end Alembic commands ###
