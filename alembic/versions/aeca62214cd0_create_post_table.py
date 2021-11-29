"""create post table

Revision ID: aeca62214cd0
Revises: 
Create Date: 2021-11-28 22:03:36.045625

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'aeca62214cd0'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('posts' , sa.Column('id', sa.Integer(),nullable=False , primary_key=True)
        ,sa.Column('title',sa.String(),nullable=False))

    pass


def downgrade():
    op.drop_table('posts')
    pass
