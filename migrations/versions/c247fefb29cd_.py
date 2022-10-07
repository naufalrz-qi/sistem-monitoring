"""empty message

Revision ID: c247fefb29cd
Revises: 3708f0f502f6
Create Date: 2022-10-05 19:25:23.428751

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c247fefb29cd'
down_revision = '3708f0f502f6'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('detail_siswa', sa.Column('qr_code', sa.Text(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('detail_siswa', 'qr_code')
    # ### end Alembic commands ###
