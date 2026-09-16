"""add vehicles table and link rides to vehicles

Revision ID: c7d8e9f01a2b
Revises: 6b7868552c83
Create Date: 2026-09-12 12:00:00.000000

"""
import uuid
from datetime import datetime, timezone
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c7d8e9f01a2b'
down_revision: Union[str, None] = '6b7868552c83'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    connection = op.get_bind()
    inspector = sa.inspect(connection)

    # 1. Create vehicles table if not exists
    if 'vehicles' not in inspector.get_table_names():
        op.create_table(
            'vehicles',
            sa.Column('id', sa.Integer(), primary_key=True),
            sa.Column('uuid', sa.String(length=36), nullable=False, unique=True),
            sa.Column('vehicle_plate', sa.String(length=20), nullable=False),
            sa.Column('vehicle_model', sa.String(length=80), nullable=False),
            sa.Column('seats', sa.Integer(), nullable=False, server_default='4'),
            sa.Column('owner_id', sa.Integer(), sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False),
            sa.Column('created_at', sa.DateTime(timezone=True), nullable=True),
            sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        )

    # 2. Add vehicle_id column to rides table if not exists
    columns = [col['name'] for col in inspector.get_columns('rides')]
    if 'vehicle_id' not in columns:
        with op.batch_alter_table('rides') as batch_op:
            batch_op.add_column(sa.Column('vehicle_id', sa.Integer(), sa.ForeignKey('vehicles.id', ondelete='RESTRICT', name='fk_rides_vehicle_id'), nullable=True))

    # 3. Data migration: Migrate existing rides vehicle details to vehicles table & update rides.vehicle_id
    connection = op.get_bind()

    # Query distinct vehicle details from rides
    rides = connection.execute(sa.text("SELECT id, owner_id, vehicle_plate, vehicle_model, seats FROM rides")).fetchall()

    vehicle_map = {}  # (owner_id, plate, model) -> vehicle_id
    now_str = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")

    for ride in rides:
        ride_id, owner_id, plate, model, seats = ride[0], ride[1], ride[2], ride[3], ride[4]
        key = (owner_id, plate, model)

        if key not in vehicle_map:
            v_uuid = str(uuid.uuid4())
            connection.execute(
                sa.text(
                    "INSERT INTO vehicles (uuid, vehicle_plate, vehicle_model, seats, owner_id, created_at, updated_at) "
                    "VALUES (:uuid, :plate, :model, :seats, :owner_id, :now, :now)"
                ),
                {
                    "uuid": v_uuid,
                    "plate": plate,
                    "model": model,
                    "seats": seats,
                    "owner_id": owner_id,
                    "now": now_str,
                }
            )
            # Retrieve inserted vehicle id
            veh_row = connection.execute(
                sa.text("SELECT id FROM vehicles WHERE uuid = :uuid"),
                {"uuid": v_uuid}
            ).fetchone()
            if veh_row:
                vehicle_map[key] = veh_row[0]

        v_id = vehicle_map.get(key)
        if v_id:
            connection.execute(
                sa.text("UPDATE rides SET vehicle_id = :v_id WHERE id = :ride_id"),
                {"v_id": v_id, "ride_id": ride_id}
            )


def downgrade() -> None:
    op.drop_column('rides', 'vehicle_id')
    op.drop_table('vehicles')
