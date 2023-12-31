"""create post tables

Revision ID: 3620477e7148
Revises: 
Create Date: 2023-12-31 21:26:09.126113

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3620477e7148'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table("posts", sa.Column("id", sa.Integer(), nullable=False, primary_key=True),
                    sa.Column("title", sa.String(),nullable=False))
    pass


def downgrade() -> None:
    op.drop_table("posts")
    pass
