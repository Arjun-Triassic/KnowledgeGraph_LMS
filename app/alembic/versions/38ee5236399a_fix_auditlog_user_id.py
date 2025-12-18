"""fix auditlog user_id 

Revision ID: 38ee5236399a
Revises: a580e06a0b1c
Create Date: 2025-12-17 10:05:10.818327

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "38ee5236399a"
down_revision = 'a580e06a0b1c'
branch_labels = None
depends_on = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass

