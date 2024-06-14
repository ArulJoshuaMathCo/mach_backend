"""Update clientcentric column type from string to int

Revision ID: ecf7cc7bd702
Revises: 439f6c9cb6d5
Create Date: 2024-06-14 17:33:50.092725

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ecf7cc7bd702'
down_revision: Union[str, None] = '439f6c9cb6d5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade():
    # Change the data type of the ClientCentric column to Integer
    pass

def downgrade():
    # Revert the data type of the ClientCentric column to String
    pass