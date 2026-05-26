"""Add User model

Revision ID: b3c4d5e6f7a8
Revises: f2a1d9b3c4e7
Create Date: 2026-05-12 21:10:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'b3c4d5e6f7a8'
down_revision = 'f2a1d9b3c4e7'
branch_labels = None
depends_on = None

def upgrade():
    # Crear la tabla users
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('email', sa.String(length=120), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)
    
    # Crear foreign key en historial_documentos
    op.create_foreign_key(
        'fk_historial_documentos_user_id', 
        'historial_documentos', 'users', 
        ['user_id'], ['id']
    )

def downgrade():
    op.drop_constraint('fk_historial_documentos_user_id', 'historial_documentos', type_='foreignkey')
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.drop_table('users')
