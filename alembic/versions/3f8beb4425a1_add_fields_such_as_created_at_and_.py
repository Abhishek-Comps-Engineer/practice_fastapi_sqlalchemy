"""add fields such as created_at and published in posts table

Revision ID: 3f8beb4425a1
Revises: 3877e039fb68
Create Date: 2025-08-30 16:32:28.503591

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3f8beb4425a1'
down_revision: Union[str, Sequence[str], None] = '3877e039fb68'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column("published",
        sa.Boolean(),nullable=False, server_default="TRUE"))
    op.add_column('posts',sa.Column("created_at", sa.TIMESTAMP(timezone=True),nullable=False, server_default=sa.text('Now()')))
    pass


def downgrade() -> None:
    op.drop_column('posts','published')
    op.drop_column('posts','created_at')
    pass
