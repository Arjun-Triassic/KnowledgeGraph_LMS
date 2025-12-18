"""fix auditlog user_id fk and make nullable

Revision ID: a580e06a0b1c
Revises: f63d286470cd
Create Date: 2025-12-17 10:02:19.943452

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "a580e06a0b1c"
down_revision = 'f63d286470cd'
branch_labels = None
depends_on = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass

