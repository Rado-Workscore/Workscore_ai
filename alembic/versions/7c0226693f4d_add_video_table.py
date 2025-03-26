"""Add video table

Revision ID: 7c0226693f4d
Revises: 163bb606a144
Create Date: 2025-03-24 21:45:45.876368

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7c0226693f4d'
down_revision: Union[str, None] = '163bb606a144'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "videos",
        sa.Column("id", sa.Integer(), primary_key=True, index=True),
        sa.Column("filename", sa.String(), nullable=False),
        sa.Column("warehouse_id", sa.Integer(), sa.ForeignKey("warehouses.id"), nullable=False),
        sa.Column("camera_id", sa.Integer(), sa.ForeignKey("cameras.id"), nullable=False),
        sa.Column("uploaded_at", sa.DateTime(), nullable=False),
        sa.Column("is_processed", sa.Boolean(), nullable=False)
    )


def downgrade() -> None:
    op.drop_table("videos")

