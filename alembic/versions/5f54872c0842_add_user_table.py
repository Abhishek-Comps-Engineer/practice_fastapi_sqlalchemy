"""add user table

Revision ID: 5f54872c0842
Revises: 02c68bac86e8
Create Date: 2025-08-30 16:00:04.699664

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5f54872c0842'
down_revision: Union[str, Sequence[str], None] = '02c68bac86e8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('users',
                    sa.Column('id',sa.Integer(),nullable=False,primary_key=True),
                    sa.Column('email',sa.Integer(),nullable=False),
                    sa.Column('password',sa.String(),nullable=False),
                    sa.Column('created_at',sa.TIMESTAMP(timezone=True),
                              server_default=sa.text('now()'),nullable=False),
                    sa.UniqueConstraint('email'))
    
    pass


def downgrade() -> None:
    op.drop_table("users")
    pass
