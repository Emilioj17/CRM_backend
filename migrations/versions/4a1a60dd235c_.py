"""empty message

Revision ID: 4a1a60dd235c
Revises: 86d250235728
Create Date: 2021-07-09 16:44:41.505937

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4a1a60dd235c'
down_revision = '86d250235728'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('contacts', sa.Column('rut', sa.String(length=100), nullable=False))
    op.add_column('users', sa.Column('rut', sa.String(length=100), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'rut')
    op.drop_column('contacts', 'rut')
    # ### end Alembic commands ###
