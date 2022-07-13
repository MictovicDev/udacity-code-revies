"""empty message

Revision ID: 199c2a4482a2
Revises: 4cfa01665bb2
Create Date: 2022-07-10 01:13:55.374158

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '199c2a4482a2'
down_revision = '4cfa01665bb2'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Artist', sa.Column('seeking_description', sa.String(length=120), nullable=True))
    op.drop_column('Artist', 'seeking_talent')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Artist', sa.Column('seeking_talent', sa.BOOLEAN(), autoincrement=False, nullable=True))
    op.drop_column('Artist', 'seeking_description')
    # ### end Alembic commands ###
