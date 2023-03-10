"""added username

Revision ID: 3981d0ae65c0
Revises: 7f32a4edce76
Create Date: 2022-12-29 14:11:32.228689

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3981d0ae65c0'
down_revision = '7f32a4edce76'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('username', sa.String(length=20), nullable=False))
        batch_op.create_unique_constraint(None, ['username'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='unique')
        batch_op.drop_column('username')

    # ### end Alembic commands ###
