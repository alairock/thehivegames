"""add user passphrase constraint

Revision ID: 0657b36a1693
Revises: b3d881873b39
Create Date: 2021-07-05 21:31:25.632461

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0657b36a1693'
down_revision = 'b3d881873b39'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('passphrase', sa.Text(), nullable=True))
    op.create_index('username_passphrase_uniq', 'users', ['username', 'passphrase'], unique=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('username_passphrase_uniq', table_name='users')
    op.drop_column('users', 'passphrase')
    # ### end Alembic commands ###
