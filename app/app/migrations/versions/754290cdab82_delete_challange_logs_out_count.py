"""delete challange_logs.out_count

Revision ID: 754290cdab82
Revises: 7f7ef83e467c
Create Date: 2022-03-15 23:56:37.725482

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '754290cdab82'
down_revision = '7f7ef83e467c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('challange_logs', 'out_count')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('challange_logs', sa.Column('out_count', mysql.INTEGER(), autoincrement=False, nullable=True))
    # ### end Alembic commands ###
