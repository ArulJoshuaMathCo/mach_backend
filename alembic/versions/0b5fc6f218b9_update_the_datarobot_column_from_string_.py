"""update the datarobot column from string to int

Revision ID: 0b5fc6f218b9
Revises: ecf7cc7bd702
Create Date: 2024-06-14 22:25:07.279167

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0b5fc6f218b9'
down_revision: Union[str, None] = 'ecf7cc7bd702'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # Ensure column name is properly quoted for SQL
    column = "DataRobot"
    quoted_column = f'"{column}"'
    
    # Update empty strings to NULL
    op.execute(f"""
    UPDATE skills1
    SET {quoted_column} = NULL
    WHERE {quoted_column} = '';
    """)

    # Alter the column type
    op.alter_column(
        'skills1',
        column,
        existing_type=sa.VARCHAR(),
        type_=sa.INTEGER(),
        postgresql_using=f"{quoted_column}::INTEGER"
    )

def downgrade():
    # Ensure column name is properly quoted for SQL
    column = "DataRobot"
    quoted_column = f'"{column}"'
    
    # Revert column type change
    op.alter_column(
        'skills1',
        column,
        existing_type=sa.INTEGER(),
        type_=sa.VARCHAR()
    )

    # Optionally, set NULLs back to empty strings if needed (reverse operation)
    op.execute(f"""
    UPDATE skills1
    SET {quoted_column} = ''
    WHERE {quoted_column} IS NULL;
    """)
    