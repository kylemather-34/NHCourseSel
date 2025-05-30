"""Updated models with relationships

Revision ID: 68599b2e7355
Revises: 5139cbd4df81
Create Date: 2024-11-17 09:31:42.950880

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '68599b2e7355'
down_revision = '5139cbd4df81'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('course', schema=None) as batch_op:
        batch_op.alter_column('id',
               existing_type=sa.INTEGER(),
               nullable=False,
               autoincrement=True)
        batch_op.alter_column('course_code',
               existing_type=sa.TEXT(),
               type_=sa.String(length=20),
               nullable=False)
        batch_op.alter_column('course_name',
               existing_type=sa.TEXT(),
               type_=sa.String(length=200),
               nullable=False)
        batch_op.alter_column('credits',
               existing_type=sa.REAL(),
               type_=sa.Float(),
               existing_nullable=True)
        batch_op.alter_column('description',
               existing_type=sa.TEXT(),
               nullable=False)
        batch_op.drop_index('unique_course_code')
        batch_op.drop_constraint('unique_course_entry', type_='unique')
        batch_op.create_index(batch_op.f('ix_course_course_code'), ['course_code'], unique=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('course', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_course_course_code'))
        batch_op.create_unique_constraint('unique_course_entry', ['course_code'])
        batch_op.create_index('unique_course_code', ['course_code'], unique=1)
        batch_op.alter_column('description',
               existing_type=sa.TEXT(),
               nullable=True)
        batch_op.alter_column('credits',
               existing_type=sa.Float(),
               type_=sa.REAL(),
               existing_nullable=True)
        batch_op.alter_column('course_name',
               existing_type=sa.String(length=200),
               type_=sa.TEXT(),
               nullable=True)
        batch_op.alter_column('course_code',
               existing_type=sa.String(length=20),
               type_=sa.TEXT(),
               nullable=True)
        batch_op.alter_column('id',
               existing_type=sa.INTEGER(),
               nullable=True,
               autoincrement=True)

    # ### end Alembic commands ###
