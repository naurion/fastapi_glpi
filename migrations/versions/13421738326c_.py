"""empty message

Revision ID: 13421738326c
Revises: 564ef857f2c8
Create Date: 2023-07-21 13:41:36.546637

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '13421738326c'
down_revision = '564ef857f2c8'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('tickets', sa.Column('glpi_url', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('tickets', 'glpi_url')
    # ### end Alembic commands ###
