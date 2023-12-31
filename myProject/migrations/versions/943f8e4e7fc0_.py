"""empty message

Revision ID: 943f8e4e7fc0
Revises: 2b7a3bc84045
Create Date: 2023-11-29 04:28:15.610651

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '943f8e4e7fc0'
down_revision = '2b7a3bc84045'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('book', schema=None) as batch_op:
        batch_op.add_column(sa.Column('checked_out_by_id', sa.Integer(), nullable=True))
        batch_op.create_foreign_key('fk_checked_out_by', 'user', ['checked_out_by_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('book', schema=None) as batch_op:
        batch_op.drop_constraint('fk_checked_out_by', type_='foreignkey')
        batch_op.drop_column('checked_out_by_id')
    # ### end Alembic commands ###

