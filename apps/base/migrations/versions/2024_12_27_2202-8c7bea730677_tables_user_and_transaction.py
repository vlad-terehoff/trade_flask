"""tables user and transaction

Revision ID: 8c7bea730677
Revises: 
Create Date: 2024-12-27 22:02:02.407149

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '8c7bea730677'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    sa.Enum('WAITING', 'CONFIRMED', 'CANCELLED', 'EXPIRED', name='transactionstatus').create(op.get_bind())
    sa.Enum('ADMIN', 'ORDINARY', name='userroles').create(op.get_bind())
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=255), nullable=False),
    sa.Column('password', sa.String(length=255), nullable=False),
    sa.Column('balance', sa.Numeric(), nullable=False),
    sa.Column('commission', sa.Numeric(precision=1, scale=3), nullable=False),
    sa.Column('url_webhook', sa.String(length=255), nullable=True),
    sa.Column('usdt_wallet', sa.String(length=255), nullable=True),
    sa.Column('role', postgresql.ENUM('ADMIN', 'ORDINARY', name='userroles', create_type=False), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('transactions',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text("TIMEZONE('utc', now())"), nullable=False),
    sa.Column('status', postgresql.ENUM('WAITING', 'CONFIRMED', 'CANCELLED', 'EXPIRED', name='transactionstatus', create_type=False), nullable=False),
    sa.Column('amount', sa.Numeric(scale=5), nullable=False),
    sa.Column('commission', sa.Numeric(scale=3), nullable=False),
    sa.CheckConstraint('amount >= 0', name='check_commission_non_negative'),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('transactions')
    op.drop_table('users')
    sa.Enum('ADMIN', 'ORDINARY', name='userroles').drop(op.get_bind())
    sa.Enum('WAITING', 'CONFIRMED', 'CANCELLED', 'EXPIRED', name='transactionstatus').drop(op.get_bind())
    # ### end Alembic commands ###