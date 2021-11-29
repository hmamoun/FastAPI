"""add last few columns to potst table

Revision ID: 2a8c9595a220
Revises: d7e8f576fbd2
Create Date: 2021-11-28 22:41:20.882433

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2a8c9595a220'
down_revision = 'd7e8f576fbd2'
branch_labels = None
depends_on = None



def upgrade():
    op.add_column('posts', sa.Column(
        'published', sa.Boolean(), nullable=False, server_default='TRUE'),)
    op.add_column('posts', sa.Column(
        'created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('NOW()')),)
    pass


def downgrade():
    op.drop_column('posts', 'published')
    op.drop_column('posts', 'created_at')
    pass