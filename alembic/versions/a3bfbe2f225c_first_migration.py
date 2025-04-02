"""First migration

Revision ID: a3bfbe2f225c
Revises: 3210452ec82f
Create Date: 2025-04-02 17:12:36.004816

"""

from typing import Sequence, Union


# revision identifiers, used by Alembic.
revision: str = "a3bfbe2f225c"
down_revision: Union[str, None] = "3210452ec82f"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
