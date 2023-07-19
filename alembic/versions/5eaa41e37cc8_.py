"""empty message

Revision ID: 5eaa41e37cc8
Revises: 9b07c086c932
Create Date: 2023-07-18 16:48:00.065792

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "5eaa41e37cc8"
down_revision = "9b07c086c932"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("tally", "bill_id")
    op.add_column("tally", sa.Column("bill_id", sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("tally", "bill_id")
    op.add_column("tally", sa.Column("bill_id", sa.Integer(), nullable=True))
    # ### end Alembic commands ###