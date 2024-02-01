"""screw password hashing

Revision ID: 1706f079d564
Revises: f22d1578d31d
Create Date: 2024-01-27 22:55:40.167725

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "1706f079d564"
down_revision: Union[str, None] = "f22d1578d31d"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("users", sa.Column("password", sa.String(), nullable=False))
    op.drop_constraint("users_encrypted_password_key", "users", type_="unique")
    op.drop_column("users", "encrypted_password")
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "users",
        sa.Column(
            "encrypted_password",
            sa.VARCHAR(),
            autoincrement=False,
            nullable=False,
        ),
    )
    op.create_unique_constraint(
        "users_encrypted_password_key", "users", ["encrypted_password"]
    )
    op.drop_column("users", "password")
    # ### end Alembic commands ###
