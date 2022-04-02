"""add watchlist

Revision ID: 5536aed2d41c
Revises: f5a5d0ebd0a1
Create Date: 2022-04-01 10:49:46.630273

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5536aed2d41c'
down_revision = 'f5a5d0ebd0a1'
branch_labels = None
depends_on = None


def upgrade():

    op.create_table('watchlist',
                    sa.Column('user_id', sa.Integer(),nullable=False),
                    sa.Column('crypto_id', sa.String(),nullable=False),
                    sa.Column('id',sa.Integer()),
                    sa.ForeignKeyConstraint(('user_id',),['users.id'],),
                    sa.ForeignKeyConstraint(('crypto_id',), ['cryptocurrency.id'], ),
                    sa.PrimaryKeyConstraint('id')
                    )



def downgrade():
    op.drop_table('watchlist')
