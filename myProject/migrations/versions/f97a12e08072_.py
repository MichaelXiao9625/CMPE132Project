"""empty message

Revision ID: f97a12e08072
Revises: 943f8e4e7fc0
Create Date: 2023-11-29 06:41:08.307385

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f97a12e08072'
down_revision = '943f8e4e7fc0'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user_books',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('book_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['book_id'], ['book.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('user_id', 'book_id')
    )
    with op.batch_alter_table('book', schema=None) as batch_op:
        batch_op.drop_constraint('fk_checked_out_by', type_='foreignkey')
        batch_op.drop_column('checked_out_by_id')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('book', schema=None) as batch_op:
        batch_op.add_column(sa.Column('checked_out_by_id', sa.INTEGER(), nullable=True))
        batch_op.create_foreign_key('fk_checked_out_by', 'user', ['checked_out_by_id'], ['id'])

    op.drop_table('user_books')
    # ### end Alembic commands ###
