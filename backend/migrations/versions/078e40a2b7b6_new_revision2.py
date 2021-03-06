"""New revision2

Revision ID: 078e40a2b7b6
Revises: 6c57db4177b5
Create Date: 2021-02-20 01:22:45.370821

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '078e40a2b7b6'
down_revision = '6c57db4177b5'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('bank_account',
    sa.Column('pk', sa.Integer(), nullable=False),
    sa.Column('api_key', sa.String(length=512), nullable=True),
    sa.PrimaryKeyConstraint('pk')
    )
    op.create_table('user',
    sa.Column('pk', sa.Integer(), nullable=False),
    sa.Column('first_name', sa.String(length=256), nullable=True),
    sa.Column('last_name', sa.String(length=256), nullable=True),
    sa.Column('email', sa.String(length=256), nullable=True),
    sa.Column('password', sa.String(length=256), nullable=True),
    sa.Column('is_active', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('pk'),
    sa.UniqueConstraint('email')
    )
    op.create_table('card',
    sa.Column('pk', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=256), nullable=True),
    sa.Column('balance', sa.Integer(), nullable=True),
    sa.Column('is_blocked', sa.Boolean(), nullable=True),
    sa.Column('limit', sa.Integer(), nullable=True),
    sa.Column('currency', sa.String(length=3), nullable=True),
    sa.Column('owner_pk', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['owner_pk'], ['bank_account.pk'], ),
    sa.PrimaryKeyConstraint('pk')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('card')
    op.drop_table('user')
    op.drop_table('bank_account')
    # ### end Alembic commands ###
