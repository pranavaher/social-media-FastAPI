"""create users table

Revision ID: 95c932a6fbde
Revises: f6bcfeef70ce
Create Date: 2024-07-30 16:24:03.904907

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '95c932a6fbde'
down_revision: Union[str, None] = 'f6bcfeef70ce'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('users', sa.Column('id', sa.Integer(), nullable=False), sa.Column('email', sa.String(), nullable=False), sa.Column('password', sa.String(), nullable=False), sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False), sa.PrimaryKeyConstraint('id'), sa.UniqueConstraint('email'))

def downgrade() -> None:
    op.drop_table('users')
