"""add role to users

Revision ID: f3a4b5c6d7e8
Revises: d8e9f01a2b3c
Create Date: 2026-09-14 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f3a4b5c6d7e8'
down_revision: Union[str, None] = 'd8e9f01a2b3c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        'users',
        sa.Column('role', sa.String(length=10), nullable=False, server_default='user'),
    )


def downgrade() -> None:
    op.drop_column('users', 'role')
