"""create phone number for user col

Revision ID: e9f819060db5
Revises:
Create Date: 2023-04-03 14:13:02.492312

"""
import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = "e9f819060db5"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("users", sa.Column("phone_number", sa.String(), nullable=True))


def downgrade() -> None:
    op.drop_column("users", "phone_number")
