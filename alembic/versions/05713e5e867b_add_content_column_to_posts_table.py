"""add content column to posts table

Revision ID: 05713e5e867b
Revises: aeca62214cd0
Create Date: 2021-11-28 22:11:45.939035

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '05713e5e867b'
down_revision = 'aeca62214cd0'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts',sa.Column('content',sa.String() , nullable=False))
    pass


def downgrade():
    op.drop_column('posts' , 'content')
    pass
