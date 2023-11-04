"""making skill name unique

Revision ID: b97c3ef125e7
Revises: 045109d52f65
Create Date: 2023-10-16 19:57:13.123491

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b97c3ef125e7'
down_revision = '045109d52f65'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(None, 'skill', ['name'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'skill', type_='unique')
    # ### end Alembic commands ###
