"""empty message

Revision ID: 502c5fa08064
Revises: 
Create Date: 2024-07-13 14:33:18.293355

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '502c5fa08064'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('property', schema=None) as batch_op:
        batch_op.alter_column('rate_number',
               existing_type=sa.INTEGER(),
               type_=sa.String(),
               existing_nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('property', schema=None) as batch_op:
        batch_op.alter_column('rate_number',
               existing_type=sa.String(),
               type_=sa.INTEGER(),
               existing_nullable=False)

    # ### end Alembic commands ###