from typing import Optional
from sqlalchemy import select
from app.repositories.base_repository import BaseRepository
from app.models.user import User

class UserRepository(BaseRepository[User]):
    def __init__(self):
        super().__init__(User)

    def get_by_email(self, email: str) -> Optional[User]:
        stmt = select(self.model_class).where(self.model_class.email == email)
        return self.session.scalar(
            stmt, 
            bind_arguments={"bind": self._get_read_engine()}
        )
