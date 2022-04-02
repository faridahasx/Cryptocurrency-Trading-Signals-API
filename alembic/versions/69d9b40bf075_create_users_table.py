"""create users table

Revision ID: 69d9b40bf075
Revises: 
Create Date: 2022-04-01 10:29:08.187361

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '69d9b40bf075'
down_revision = None
branch_labels = None
depends_on = None



def upgrade():
    op.create_table('users',
                    sa.Column('id',sa.Integer(),nullable=False,primary_key=True),
                    sa.Column('email',sa.String(),nullable=False,index=True,unique=True),
                    sa.Column('username',sa.String(),nullable=False,index=True),
                    sa.Column('password',sa.String(),nullable=False),
                    sa.Column('created_at',sa.TIMESTAMP(timezone=True),nullable=False,server_default=sa.text('now()')))



def downgrade():
    op.drop_table('users')




