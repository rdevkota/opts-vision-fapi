"""empty message

Revision ID: 521084d09ca1
Revises: 
Create Date: 2022-01-28 17:38:10.499047

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '521084d09ca1'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('daily_history', 'ticker',
               existing_type=sa.VARCHAR(length=255),
               nullable=False)
    op.alter_column('daily_history', 'day',
               existing_type=sa.VARCHAR(length=255),
               nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('daily_history', 'day',
               existing_type=sa.VARCHAR(length=255),
               nullable=True)
    op.alter_column('daily_history', 'ticker',
               existing_type=sa.VARCHAR(length=255),
               nullable=True)
    # ### end Alembic commands ###
