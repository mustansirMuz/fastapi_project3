"""create address_id to users

Revision ID: c42b3d4feb22
Revises: 944196d03095
Create Date: 2023-04-03 14:25:36.051025

"""
import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = "c42b3d4feb22"
down_revision = "944196d03095"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("users", sa.Column("address_id", sa.Integer(), nullable=True))
    op.create_foreign_key(
        "address_users_fk",
        source_table="users",
        referent_table="address",
        local_cols=["address_id"],
        remote_cols=["id"],
        ondelete="CASCADE",
    )


def downgrade() -> None:
    op.drop_constraint("address_users_fk", table_name="users")
    op.drop_column("users", "address_id")
