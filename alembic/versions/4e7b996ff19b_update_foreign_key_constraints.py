"""Update foreign key constraints

Revision ID: 4e7b996ff19b
Revises: 83ee1b5ee7c0
Create Date: 2024-09-10 11:59:28.823697

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4e7b996ff19b'
down_revision: Union[str, None] = '83ee1b5ee7c0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_constraint('LoginAttempt_login_method_id_fkey',
                       'LoginMethod', type_='foreignkey')

    # Add the foreign key constraint with CASCADE delete
    op.create_foreign_key(
        'LoginAttempt_login_method_id_fkey',  # Name of the foreign key constraint
        'LoginMethod',  # Source table
        'LoginAttempt',  # Target table
        ['login_method_id'],  # Source column
        ['id'],  # Target column
        ondelete='CASCADE'  # Set to CASCADE on delete
    )


def downgrade() -> None:
    pass
