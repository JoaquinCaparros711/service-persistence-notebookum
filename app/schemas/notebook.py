from app.schemas import ma
from app.models.notebook import Notebook


class NotebookSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Notebook
        load_instance = True
        include_fk = True


notebook_schema = NotebookSchema()
notebooks_schema = NotebookSchema(many=True)
