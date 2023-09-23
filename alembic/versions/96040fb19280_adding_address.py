"""adding address

Revision ID: 96040fb19280
Revises: 9a33506b94f1
Create Date: 2023-09-23 14:12:01.668903

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '96040fb19280'
down_revision = '9a33506b94f1'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column(
        'mobile_number', sa.Integer(), nullable=True))
    op.add_column('user', sa.Column('address_block',
                  sa.String(length=50), nullable=True))
    op.add_column('user', sa.Column('address_street',
                  sa.String(length=250), nullable=True))
    op.add_column('user', sa.Column('recidential_country',
                  sa.String(length=60), nullable=True))
    op.add_column('user', sa.Column(
        'nationality', sa.String(length=70), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'nationality')
    op.drop_column('user', 'recidential_country')
    op.drop_column('user', 'address_street')
    op.drop_column('user', 'address_block')
    op.drop_column('user', 'mobile_number')
    # ### end Alembic commands ###
