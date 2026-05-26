from app.schemas import ma
from app.models.document import HistorialDocumento


class DocumentSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = HistorialDocumento
        load_instance = True
        include_fk = True


document_schema = DocumentSchema()
documents_schema = DocumentSchema(many=True)
