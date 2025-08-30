"""add Title to Posts table

Revision ID: 3877e039fb68
Revises: ccad62fa8b2d
Create Date: 2025-08-30 16:24:59.479880

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3877e039fb68'
down_revision: Union[str, Sequence[str], None] = 'ccad62fa8b2d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts',sa.Column('title',sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts','title')
    pass
