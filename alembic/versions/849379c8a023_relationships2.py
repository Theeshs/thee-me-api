"""relationships2

Revision ID: 849379c8a023
Revises: 7236779cf2fa
Create Date: 2023-10-28 00:39:01.521233

"""
import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = "849379c8a023"
down_revision = "7236779cf2fa"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "user_skill_association", sa.Column("user_id", sa.Integer(), nullable=True)
    )
    op.add_column(
        "user_skill_association", sa.Column("skill_id", sa.Integer(), nullable=True)
    )
    op.drop_constraint(
        "user_skill_association_skill_key", "user_skill_association", type_="unique"
    )
    op.create_unique_constraint(None, "user_skill_association", ["skill_id"])
    op.drop_constraint(
        "user_skill_association_skill_fkey",
        "user_skill_association",
        type_="foreignkey",
    )
    op.drop_constraint(
        "user_skill_association_user_fkey", "user_skill_association", type_="foreignkey"
    )
    op.create_foreign_key(
        None, "user_skill_association", "user", ["user_id"], ["id"], ondelete="CASCADE"
    )
    op.create_foreign_key(
        None,
        "user_skill_association",
        "skill",
        ["skill_id"],
        ["id"],
        ondelete="CASCADE",
    )
    op.drop_column("user_skill_association", "skill")
    op.drop_column("user_skill_association", "user")
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "user_skill_association",
        sa.Column("user", sa.INTEGER(), autoincrement=False, nullable=True),
    )
    op.add_column(
        "user_skill_association",
        sa.Column("skill", sa.INTEGER(), autoincrement=False, nullable=True),
    )
    op.drop_constraint(None, "user_skill_association", type_="foreignkey")
    op.drop_constraint(None, "user_skill_association", type_="foreignkey")
    op.create_foreign_key(
        "user_skill_association_user_fkey",
        "user_skill_association",
        "user",
        ["user"],
        ["id"],
        ondelete="CASCADE",
    )
    op.create_foreign_key(
        "user_skill_association_skill_fkey",
        "user_skill_association",
        "skill",
        ["skill"],
        ["id"],
        ondelete="CASCADE",
    )
    op.drop_constraint(None, "user_skill_association", type_="unique")
    op.create_unique_constraint(
        "user_skill_association_skill_key", "user_skill_association", ["skill"]
    )
    op.drop_column("user_skill_association", "skill_id")
    op.drop_column("user_skill_association", "user_id")
    # ### end Alembic commands ###
