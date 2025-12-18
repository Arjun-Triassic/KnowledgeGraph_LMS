from typing import List

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.common.base_service import BaseService
from app.core.models.module import Module
from app.core.models.user import User
from app.schemas.module import ModuleCreate, ModuleUpdate


class ModuleService(BaseService[Module]):
    """
    Business logic for modules.
    """

    model = Module

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session)

    async def create_module(self, payload: ModuleCreate, _current_user: User) -> Module:
        return await self.create(payload.dict())

    async def list_by_course(self, course_id: int) -> List[Module]:
        return await self.list(filters={"course_id": course_id})

    async def get_module(self, module_id: int) -> Module:
        module = await self.get_by_id(module_id)
        if not module:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Module not found")
        return module

    async def update_module(self, module_id: int, payload: ModuleUpdate) -> Module:
        module = await self.get_module(module_id)
        return await self.update(module, payload.dict(exclude_unset=True))



