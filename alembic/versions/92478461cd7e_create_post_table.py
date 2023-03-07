"""create post table

Revision ID: 92478461cd7e
Revises: 
Create Date: 2023-03-07 11:56:01.358360

Created this file with the command line: alembic revision -m 'create post table'
Then after this file is updated, run: alembic upgrade 92478461cd7e

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '92478461cd7e'
down_revision = None
branch_labels = None
depends_on = None

#See API Details -> DDL Internals in the Alembic documentation
def upgrade():
    op.create_table('posts',
                    sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
                    sa.Column('title', sa.String(), nullable=False)
                    )
    pass


def downgrade():
    op.drop_table('posts')
    pass
