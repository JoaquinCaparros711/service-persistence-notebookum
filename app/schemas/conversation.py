from app.schemas import ma
from app.models.conversation import Conversation

class ConversationSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Conversation
        load_instance = True
        include_fk = True

conversation_schema = ConversationSchema()
conversations_schema = ConversationSchema(many=True)
