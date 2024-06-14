"""Update latest column type from string to int

Revision ID: 439f6c9cb6d5
Revises: 9c3d27ac2b13
Create Date: 2024-06-14 17:18:05.613241

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '439f6c9cb6d5'
down_revision: Union[str, None] = '9c3d27ac2b13'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    columns_to_update = [
        "Agile: Scrum", "Agile: Kanban", "PM Tools: JIRA", "GCP Pub/Sub", "scrum",
        "Application CI/CD", "ETL / ELT", "asp_skills", "Discipline & Integrity",
        "Initiative & Ownership", "Adaptability", "Teamwork", "Innovative Thinking",
        "Curiosity & Learning Agility", "Problem Solving", "Result Orientation", "Quality Focus"
    ]

    for column in columns_to_update:
        # Ensure column name is properly quoted for SQL
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
    columns_to_update = [
        "Agile: Scrum", "Agile: Kanban", "PM Tools: JIRA", "GCP Pub/Sub", "scrum",
        "Application CI/CD", "ETL / ELT", "asp_skills", "Discipline & Integrity",
        "Initiative & Ownership", "Adaptability", "Teamwork", "Innovative Thinking",
        "Curiosity & Learning Agility", "Problem Solving", "Result Orientation", "Quality Focus"
    ]

    for column in columns_to_update:
        # Ensure column name is properly quoted for SQL
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
