"""Add title field to future_plans table

Revision ID: add_title_field_to_future_plans
Revises: 43e8f5ed2be4
Create Date: 2025-05-20 10:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'add_title_field_to_future_plans'
down_revision = '43e8f5ed2be4'
branch_labels = None
depends_on = None


def upgrade():
    # Add title column (initially nullable)
    with op.batch_alter_table('future_plans', schema=None) as batch_op:
        batch_op.add_column(sa.Column('title', sa.Text(), nullable=True))
    
    # Copy description to title for existing records
    op.execute("UPDATE future_plans SET title = description")
    
    # Make title not nullable after populating it
    with op.batch_alter_table('future_plans', schema=None) as batch_op:
        batch_op.alter_column('title', nullable=False)


def downgrade():
    # Drop the title column
    with op.batch_alter_table('future_plans', schema=None) as batch_op:
        batch_op.drop_column('title')
