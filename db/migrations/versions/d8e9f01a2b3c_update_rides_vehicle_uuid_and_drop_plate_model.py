"""update rides to use vehicle_uuid and drop vehicle_plate and vehicle_model

Revision ID: d8e9f01a2b3c
Revises: c7d8e9f01a2b
Create Date: 2026-09-12 14:00:00.000000

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd8e9f01a2b3c'
down_revision: Union[str, None] = 'c7d8e9f01a2b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 1. Add vehicle_uuid column with foreign key to vehicles.uuid
    with op.batch_alter_table('rides', schema=None) as batch_op:
        batch_op.add_column(sa.Column('vehicle_uuid', sa.String(length=36), nullable=True))
        batch_op.create_foreign_key('fk_rides_vehicle_uuid', 'vehicles', ['vehicle_uuid'], ['uuid'], ondelete='RESTRICT')

    # 2. Populate vehicle_uuid from vehicles table using vehicle_id if available
    connection = op.get_bind()
    connection.execute(sa.text("""
        UPDATE rides
        SET vehicle_uuid = (
            SELECT vehicles.uuid FROM vehicles WHERE vehicles.id = rides.vehicle_id
        )
        WHERE rides.vehicle_id IS NOT NULL
    """))

    # 3. Drop vehicle_plate, vehicle_model, and vehicle_id columns
    with op.batch_alter_table('rides', schema=None) as batch_op:
        batch_op.drop_column('vehicle_plate')
        batch_op.drop_column('vehicle_model')
        batch_op.drop_column('vehicle_id')


def downgrade() -> None:
    with op.batch_alter_table('rides', schema=None) as batch_op:
        batch_op.add_column(sa.Column('vehicle_id', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('vehicle_plate', sa.String(length=20), nullable=True))
        batch_op.add_column(sa.Column('vehicle_model', sa.String(length=80), nullable=True, server_default=''))
        batch_op.create_foreign_key('fk_rides_vehicle_id', 'vehicles', ['vehicle_id'], ['id'], ondelete='RESTRICT')

    connection = op.get_bind()
    connection.execute(sa.text("""
        UPDATE rides
        SET vehicle_id = (
            SELECT vehicles.id FROM vehicles WHERE vehicles.uuid = rides.vehicle_uuid
        ),
        vehicle_plate = (
            SELECT vehicles.vehicle_plate FROM vehicles WHERE vehicles.uuid = rides.vehicle_uuid
        ),
        vehicle_model = (
            SELECT vehicles.vehicle_model FROM vehicles WHERE vehicles.uuid = rides.vehicle_uuid
        )
        WHERE rides.vehicle_uuid IS NOT NULL
    """))

    with op.batch_alter_table('rides', schema=None) as batch_op:
        batch_op.drop_column('vehicle_uuid')
