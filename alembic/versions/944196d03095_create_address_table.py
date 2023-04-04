"""Create address table

Revision ID: 944196d03095
Revises: e9f819060db5
Create Date: 2023-04-03 14:20:32.463612

"""
import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = "944196d03095"
down_revision = "e9f819060db5"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "address",
        sa.Column("id", sa.Integer(), nullable=False, primary_key=True),
        sa.Column("address1", sa.String(), nullable=False),
        sa.Column("address2", sa.String(), nullable=False),
        sa.Column("city", sa.String(), nullable=False),
        sa.Column("state", sa.String(), nullable=False),
        sa.Column("country", sa.String(), nullable=False),
        sa.Column("postalcode", sa.String(), nullable=False),
    )


def downgrade() -> None:
    op.drop_table("address")
