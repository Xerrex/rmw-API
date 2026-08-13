"""Add vehicle_model and status columns to rides

Revision ID: a1b2c3d4e5f6
Revises: ce64a593451e
Create Date: 2026-08-13 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a1b2c3d4e5f6'
down_revision: Union[str, None] = 'ce64a593451e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('rides', sa.Column('vehicle_model', sa.String(length=80), nullable=False, server_default=""))
    op.add_column('rides', sa.Column('status', sa.String(length=15), nullable=False, server_default="upcoming"))


def downgrade() -> None:
    op.drop_column('rides', 'status')
    op.drop_column('rides', 'vehicle_model')
