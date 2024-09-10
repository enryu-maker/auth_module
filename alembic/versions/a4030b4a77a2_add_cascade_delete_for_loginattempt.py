"""Add cascade delete for LoginAttempt

Revision ID: a4030b4a77a2
Revises: 4e7b996ff19b
Create Date: 2024-09-10 12:16:59.800888

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a4030b4a77a2'
down_revision: Union[str, None] = '4e7b996ff19b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_constraint('LoginAttempt_login_method_id_fkey',
                       'LoginAttempt', type_='foreignkey')

    # Create a new foreign key constraint with CASCADE on delete
    op.create_foreign_key(
        'LoginAttempt_login_method_id_fkey',
        'LoginAttempt',
        'LoginMethod',
        ['login_method_id'],
        ['id'],
        ondelete='CASCADE'
    )


def downgrade() -> None:
    pass
