from __future__ import annotations

import logging
from typing import Any, Dict, Generic, Iterable, List, Optional, Type, TypeVar

from sqlalchemy import Select, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db.base import Base


logger = logging.getLogger(__name__)

TModel = TypeVar("TModel", bound=Base)


class BaseService(Generic[TModel]):
    """
    Generic async CRUD service.

    All concrete services must set ``model`` to an ORM model class and should
    expose higher-level business methods that wrap these primitives.
    """

    model: Type[TModel]

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    # ---- Core helpers -------------------------------------------------

    def _base_select(self) -> Select:
        return select(self.model)

    # ---- CRUD ---------------------------------------------------------

    async def create(self, data: Dict[str, Any]) -> TModel:
        instance = self.model(**data)  # type: ignore[arg-type]
        self.session.add(instance)
        await self.session.commit()
        await self.session.refresh(instance)
        logger.debug("Created %s with id=%s", self.model.__name__, getattr(instance, "id", None))
        return instance

    async def get_by_id(self, id_: Any) -> Optional[TModel]:
        instance = await self.session.get(self.model, id_)
        return instance

    async def list(
        self,
        filters: Optional[Dict[str, Any]] = None,
        offset: int = 0,
        limit: int = 100,
    ) -> List[TModel]:
        stmt = self._base_select()
        if filters:
            for field, value in filters.items():
                if value is None:
                    continue
                column = getattr(self.model, field, None)
                if column is not None:
                    stmt = stmt.where(column == value)

        stmt = stmt.offset(offset).limit(limit)
        result = await self.session.execute(stmt)
        return list(result.scalars().unique().all())

    async def update(self, instance: TModel, data: Dict[str, Any]) -> TModel:
        for field, value in data.items():
            if not hasattr(instance, field):
                continue
            setattr(instance, field, value)

        self.session.add(instance)
        await self.session.commit()
        await self.session.refresh(instance)
        logger.debug("Updated %s id=%s", self.model.__name__, getattr(instance, "id", None))
        return instance

    async def delete(self, instance: TModel) -> None:
        await self.session.delete(instance)
        await self.session.commit()
        logger.debug("Deleted %s id=%s", self.model.__name__, getattr(instance, "id", None))



