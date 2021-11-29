"""add foreign-key to posts table

Revision ID: d7e8f576fbd2
Revises: 0037b78e69c0
Create Date: 2021-11-28 22:30:01.683319

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd7e8f576fbd2'
down_revision = '0037b78e69c0'
branch_labels = None
depends_on = None



def upgrade():
    op.add_column('posts', sa.Column('owner_id', sa.Integer(), nullable=False))
    op.create_foreign_key('post_users_fk', source_table="posts", referent_table="users", local_cols=[
                          'owner_id'], remote_cols=['id'], ondelete="CASCADE")
    pass


def downgrade():
    op.drop_constraint('post_users_fk', table_name="posts")
    op.drop_column('posts', 'owner_id')
    pass