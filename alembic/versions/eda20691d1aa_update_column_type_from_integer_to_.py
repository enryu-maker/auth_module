"""Update column type from Integer to String

Revision ID: eda20691d1aa
Revises: 
Create Date: 2024-09-05 00:42:04.858379

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'eda20691d1aa'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column('User', 'mobile_number',
                    existing_type=sa.Integer(),
                    type_=sa.String(),
                    existing_nullable=False)


def downgrade() -> None:
    pass
