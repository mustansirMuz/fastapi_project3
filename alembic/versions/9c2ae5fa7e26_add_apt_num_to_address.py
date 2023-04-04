"""Add apt_num to address

Revision ID: 9c2ae5fa7e26
Revises: c42b3d4feb22
Create Date: 2023-04-03 14:59:45.262309

"""
import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = "9c2ae5fa7e26"
down_revision = "c42b3d4feb22"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("address", sa.Column("apt_num", sa.Integer()))


def downgrade() -> None:
    op.drop_column("address", "apt_num")
