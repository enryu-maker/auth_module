"""add image column to LoginMethod

Revision ID: 83ee1b5ee7c0
Revises: eda20691d1aa
Create Date: 2024-09-10 11:40:22.177408

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '83ee1b5ee7c0'
down_revision: Union[str, None] = 'eda20691d1aa'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('LoginMethod', sa.Column(
        'image', sa.String(length=255), nullable=True))


def downgrade() -> None:
    pass
