"""create crypto table

Revision ID: f5a5d0ebd0a1
Revises: 69d9b40bf075
Create Date: 2022-04-01 10:49:07.230370

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f5a5d0ebd0a1'
down_revision = '69d9b40bf075'
branch_labels = None
depends_on = None

def upgrade():
    op.create_table('cryptocurrency',
                    sa.Column('name', sa.String(), nullable=False),
                    sa.Column('exchange', sa.String(), nullable=False),
                    sa.Column('signal_stage', sa.String(), nullable=False),
                    sa.Column('id', sa.String(), nullable=False, primary_key=True),
                   )


def downgrade():
    op.drop_table('cryptocurrency')
