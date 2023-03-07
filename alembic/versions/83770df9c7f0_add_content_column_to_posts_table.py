"""add content column to posts table

Revision ID: 83770df9c7f0
Revises: 92478461cd7e
Create Date: 2023-03-07 12:13:22.145356

run 'alembic upgrade 83770df9c7f0'
OR 'alembic upgrade head'  Check with 'alembic heads' first.

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '83770df9c7f0'
down_revision = '92478461cd7e'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts',
                  sa.Column('content', sa.String(),nullable=False)
                  )
    pass


def downgrade():
    op.drop_column('posts','content')
    pass
