"""Initial migration


Revision ID: 6cd18623d102
Revises: 
Create Date: 2024-06-25 15:15:59.756797

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6cd18623d102'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('role', sa.String(), nullable=False, server_default='user'))
    
    # SQLite does not support modifying NOT NULL constraints directly with ALTER TABLE
    # So, we set NOT NULL using a separate statement
    op.execute('UPDATE user SET role="user" WHERE role IS NULL')
    
    # Change the column definition to NOT NULL
    op.alter_column('user', 'role', nullable=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'role')
    # ### end Alembic commands ###