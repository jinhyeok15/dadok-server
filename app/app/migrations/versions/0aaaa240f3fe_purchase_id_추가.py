"""purchase id 추가

Revision ID: 0aaaa240f3fe
Revises: da44f3318728
Create Date: 2022-03-24 16:21:18.300945

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '0aaaa240f3fe'
down_revision = 'da44f3318728'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('purchases')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('purchases',
    sa.Column('user_id', mysql.VARCHAR(length=120), nullable=False),
    sa.Column('item_id', mysql.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('created', mysql.DATETIME(), nullable=True),
    sa.Column('modified', mysql.DATETIME(), nullable=True),
    sa.Column('status', mysql.VARCHAR(length=12), nullable=True, comment='CONFIRM/SUBMIT/DELETE/PURCHASED'),
    sa.Column('id', mysql.INTEGER(), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['item_id'], ['items.id'], name='purchases_ibfk_1'),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], name='purchases_ibfk_2'),
    sa.PrimaryKeyConstraint('user_id', 'item_id'),
    mysql_collate='utf8mb4_0900_ai_ci',
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    # ### end Alembic commands ###
