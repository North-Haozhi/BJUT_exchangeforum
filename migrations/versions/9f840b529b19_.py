"""empty message

Revision ID: 9f840b529b19
Revises: f4571b811bf0
Create Date: 2020-04-21 21:34:04.043401

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9f840b529b19'
down_revision = 'f4571b811bf0'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('avatar_img', sa.String(length=120), nullable=True))
        batch_op.create_index(batch_op.f('ix_users_ID_number'), ['ID_number'], unique=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_users_ID_number'))
        batch_op.drop_column('avatar_img')

    # ### end Alembic commands ###
