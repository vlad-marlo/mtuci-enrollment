"""create note

Revision ID: 643d0f6e1cd2
Revises: 4d792e39ec67
Create Date: 2024-01-26 21:47:48.957111

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "643d0f6e1cd2"
down_revision: Union[str, None] = "4d792e39ec67"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "notes",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("text", sa.String(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("notes")
    # ### end Alembic commands ###
