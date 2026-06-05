"""sync_document_columns

Revision ID: e5f6g7h8i9j0
Revises: b3c4d5e6f7a8
Create Date: 2026-06-02 19:00:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'e5f6g7h8i9j0'
down_revision = 'b3c4d5e6f7a8'
branch_labels = None
depends_on = None

def upgrade():
    # add notebook_id column to historial_documentos table
    op.add_column('historial_documentos', sa.Column('notebook_id', sa.Integer(), nullable=True))
    op.create_foreign_key('fk_historial_documentos_notebooks', 'historial_documentos', 'notebooks', ['notebook_id'], ['id'], ondelete='CASCADE')
    op.create_index(op.f('ix_historial_documentos_notebook_id'), 'historial_documentos', ['notebook_id'], unique=False)

def downgrade():
    op.drop_index(op.f('ix_historial_documentos_notebook_id'), table_name='historial_documentos')
    op.drop_constraint('fk_historial_documentos_notebooks', 'historial_documentos', type_='foreignkey')
    op.drop_column('historial_documentos', 'notebook_id')
