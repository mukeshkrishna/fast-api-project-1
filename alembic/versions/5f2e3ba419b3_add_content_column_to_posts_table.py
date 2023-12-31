"""add content column to posts table

Revision ID: 5f2e3ba419b3
Revises: 3620477e7148
Create Date: 2023-12-31 21:39:19.644439

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5f2e3ba419b3'
down_revision: Union[str, None] = '3620477e7148'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("posts", sa.Column("content",sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column("posts", "content")
    pass
