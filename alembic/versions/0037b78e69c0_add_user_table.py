"""add user table

Revision ID: 0037b78e69c0
Revises: 05713e5e867b
Create Date: 2021-11-28 22:19:38.895249

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0037b78e69c0'
down_revision = '05713e5e867b'
branch_labels = None
depends_on = None

def upgrade():
    op.create_table('users',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('email', sa.String(), nullable=False),
                    sa.Column('password', sa.String(), nullable=False),
                    sa.Column('created_at', sa.TIMESTAMP(timezone=True),
                              server_default=sa.text('now()'), nullable=False),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('email')
                    )
    pass


def downgrade():
    op.drop_table('users')
    pass