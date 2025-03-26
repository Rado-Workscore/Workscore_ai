"""Add task table

Revision ID: 1133cf1ee806
Revises: bee4c385acaf
Create Date: 2025-03-25 17:20:07.749673
"""

from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1133cf1ee806'
down_revision: Union[str, None] = 'bee4c385acaf'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'tasks',
        sa.Column('id', sa.Integer(), primary_key=True, index=True),
        sa.Column('title', sa.String(), nullable=False),
        sa.Column('description', sa.String(), nullable=True),
        sa.Column('employee_id', sa.Integer(), sa.ForeignKey("employees.id"), nullable=False),
    )
    op.create_index('ix_tasks_id', 'tasks', ['id'], unique=False)


def downgrade() -> None:
    op.drop_index('ix_tasks_id', table_name='tasks')
    op.drop_table('tasks')



