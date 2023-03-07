"""add foreign key to posts table

Revision ID: 60788795d0d5
Revises: 5d0b0659b357
Create Date: 2023-03-07 12:32:06.655298

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '60788795d0d5'
down_revision = '5d0b0659b357'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts',sa.Column('owner_id', sa.Integer(), nullable=False))
    op.create_foreign_key('post_users_fk', source_table='posts', referent_table='users', local_cols=['owner_id'], remote_cols=['id'], ondelete="CASCADE")
                  
    pass


def downgrade():
    op.drop_constraint('post_users_fk', table_name='posts')
    op.drop_column('posts','owner_id')
    pass
