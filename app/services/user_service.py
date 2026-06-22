from typing import Any, Dict, List, Optional

from app.repositories.user_repository import UserRepository
from app.schemas.user import user_schema, users_schema

class UserService:
    def __init__(self) -> None:
        self.repository = UserRepository()

    def get_all(self) -> List[Dict[str, Any]]:
        users = self.repository.list_all()
        return users_schema.dump(users)

    def create(self, data: Dict[str, Any]) -> Dict[str, Any]:
        # Business Logic: Check for unique email
        email = data.get("email")
        if email and self.repository.get_by_email(email):
            raise ValueError("Email already in use")
            
        new_user = user_schema.load(data, session=self.repository.session)
        self.repository.create(new_user)
        return user_schema.dump(new_user)

    def get_by_id(self, user_id: int) -> Optional[Dict[str, Any]]:
        user = self.repository.get_by_id(user_id)
        if not user:
            return None
        return user_schema.dump(user)

    def update(self, user_id: int, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        user = self.repository.get_by_id(user_id)
        if not user:
            return None
            
        # Business Logic: Check for unique email if changed
        email = data.get("email")
        if email and email != user.email:
            if self.repository.get_by_email(email):
                raise ValueError("Email already in use")
                
        user = user_schema.load(data, instance=user, partial=True, session=self.repository.session)
        self.repository.update(user)
        return user_schema.dump(user)

    def delete(self, user_id: int) -> bool:
        user = self.repository.get_by_id(user_id)
        if not user:
            return False
        self.repository.delete(user)
        return True
