from typing import Type, TypeVar, Any
from databases import Database
from sqlalchemy import select, Table

TypeModel = TypeVar("TypeModel", bound=Table)


class BaseRepository:
    def __init__(self, model: Type[TypeModel], database: Database):
        self.model = model
        self.database = database

    async def create(self, instance_data: dict[str, Any]) -> dict[str, Any]:
        query = self.model.insert().values(**instance_data)
        record_id = await self.database.execute(query)
        return {**instance_data, "id": record_id}

    async def bulk_create(self, instances_data: list[dict[str, Any]]) -> None:
        query = self.model.insert()
        await self.database.execute_many(query, instances_data)

    async def get(self, **kwargs) -> dict[str, Any] | None:
        query = select(self.model).filter_by(**kwargs)
        return await self.database.fetch_one(query)

    async def get_or_create(self, instance_data: dict[str, Any]) -> dict[str, Any]:
        instance = await self.get(**instance_data)
        if instance:
            return instance
        return await self.create(instance_data)

    async def all(self) -> list[dict[str, Any]]:
        query = select(self.model)
        return await self.database.fetch_all(query)

    async def filter(self, **kwargs) -> list[dict[str, Any]]:
        query = select(self.model).filter_by(**kwargs)
        return await self.database.fetch_all(query)

    async def update(self, id: Any, instance_data: dict[str, Any]) -> None:
        query = self.model.update().where(self.model.c.id == id).values(**instance_data)
        await self.database.execute(query)

    async def role(self, role: Any, user_id: Any):
        query = self.model.update().where(self.model.c.id == user_id).values(role=role)
        await self.database.execute(query)

    async def delete(self, id: Any) -> None:
        query = self.model.delete().where(self.model.c.id == id)
        await self.database.execute(query)
