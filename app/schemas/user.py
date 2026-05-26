"""Marshmallow schemas for User models."""

from marshmallow import fields
from app.schemas import ma
from app.models.user import User

class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_instance = True

    documentos = fields.Nested("DocumentSchema", many=True, exclude=("user_id",))

user_schema = UserSchema()
users_schema = UserSchema(many=True)
