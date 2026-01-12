"""Add AI fields to tasks table

Revision ID: 002
Revises: 001
Create Date: 2026-01-13 12:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '002'
down_revision = '001'
branch_labels = None
depends_on = None


def upgrade():
    """Add AI-enhanced fields to tasks table."""
    # Add new columns for AI features
    op.add_column('tasks', sa.Column('category', sa.String(length=50), nullable=True))
    op.add_column('tasks', sa.Column('priority', sa.String(length=20), nullable=True))
    op.add_column('tasks', sa.Column('estimated_duration', sa.String(length=50), nullable=True))
    op.add_column('tasks', sa.Column('ai_tags', sa.String(length=500), nullable=True))
    op.add_column('tasks', sa.Column('ai_suggestions', sa.String(length=1000), nullable=True))


def downgrade():
    """Remove AI-enhanced fields from tasks table."""
    op.drop_column('tasks', 'ai_suggestions')
    op.drop_column('tasks', 'ai_tags')
    op.drop_column('tasks', 'estimated_duration')
    op.drop_column('tasks', 'priority')
    op.drop_column('tasks', 'category')