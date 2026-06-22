from typing import Generic, List, Optional, TypeVar

from sqlalchemy import select

from app.database import db

T = TypeVar("T")


class BaseRepository(Generic[T]):
    """Generic base repository for basic CRUD operations."""

    def __init__(self, model_class: type[T]):
        self.model_class = model_class
        # Centralizamos el acceso a db.session (Context-Local)
        self.session = db.session

    def get_by_id(self, id: int) -> Optional[T]:
        """Fetch an entity by its primary key from read replica."""
        return self.session.get(
            self.model_class, id, bind_arguments={"bind": self._get_read_engine()}
        )

    def list_all(self, **filters) -> List[T]:
        """Fetch all entities from read replica, optionally applying equality filters."""
        stmt = select(self.model_class)
        for key, value in filters.items():
            if value is not None:
                stmt = stmt.where(getattr(self.model_class, key) == value)

        return list(
            self.session.scalars(
                stmt, bind_arguments={"bind": self._get_read_engine()}
            ).all()
        )

    def create(self, instance: T) -> T:
        """Add, flush, and commit a new instance to the database (Master)."""
        self.session.add(instance)
        self.session.flush()
        self.session.commit()
        return instance

    def update(self, instance: T) -> T:
        """Flush and commit changes made to an existing instance (Master)."""
        self.session.flush()
        self.session.commit()
        return instance

    def delete(self, instance: T) -> None:
        """Delete and commit an instance from the database (Master)."""
        self.session.delete(instance)
        self.session.flush()
        self.session.commit()

    def _get_read_engine(self):
        """Helper to get the read replica engine if configured, else fallback to primary."""
        return db.engines.get("read_replica", db.engine)
