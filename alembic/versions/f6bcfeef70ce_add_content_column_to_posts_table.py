"""add content column to posts table

Revision ID: f6bcfeef70ce
Revises: a23349e61b66
Create Date: 2024-07-30 16:14:01.378842

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f6bcfeef70ce'
down_revision: Union[str, None] = 'a23349e61b66'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("posts", sa.Column("content", sa.String(), nullable=False))


def downgrade() -> None:
    op.drop_column("posts", "content")
