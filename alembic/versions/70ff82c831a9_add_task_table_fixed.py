"""Add task table (fixed)

Revision ID: 70ff82c831a9
Revises: 1133cf1ee806
Create Date: 2025-03-25 17:47:49.947096

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '70ff82c831a9'
down_revision: Union[str, None] = '1133cf1ee806'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass



def downgrade() -> None:
    op.drop_index(op.f('ix_tasks_id'), table_name='tasks')
    op.drop_table('tasks')
