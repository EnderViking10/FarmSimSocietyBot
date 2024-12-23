"""Added servers table

Revision ID: 54b9c6aacef2
Revises: 8a1b92c2b346
Create Date: 2024-12-01 03:18:25.358373

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '54b9c6aacef2'
down_revision: Union[str, None] = '8a1b92c2b346'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user_servers',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('server_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['server_id'], ['servers.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('user_id', 'server_id')
    )
    op.add_column('servers', sa.Column('name', sa.String(), nullable=False))
    op.add_column('servers', sa.Column('map', sa.String(), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('servers', 'map')
    op.drop_column('servers', 'name')
    op.drop_table('user_servers')
    # ### end Alembic commands ###
