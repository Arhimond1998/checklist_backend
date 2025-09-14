import datetime
from typing import Any, Generic, Type, TypeVar

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy import select, delete, Select, cast, Date
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.elements import BinaryExpression

from src.core.database import Base
from src.schemas.base import Filters

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class RepositoryBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(
        self,
        model: Type[ModelType],
        db: AsyncSession,
    ):
        """
        CRUD object with default methods to Create, Read, Update, Delete (CRUD).

        **Parameters**

        * `model`: A SQLAlchemy model class
        * `schema`: A Pydantic model (schema) class
        """
        self.model = model
        self.db = db

    async def get(self, *args: Any, **kwargs: Any) -> ModelType | None:
        result = await self.db.execute(
            select(self.model).filter(*args).filter_by(**kwargs)
        )
        return result.scalars().first()

    async def get_multi(
        self,
        *args: Any,
        filters: list[BinaryExpression] = None,
        orders: list[BinaryExpression] = None,
        **kwargs,
    ) -> list[ModelType]:
        filters = [] if filters is None else filters
        statement = (
            select(self.model).filter(*args).filter(*filters).filter_by(**kwargs)
        )
        if orders:
            statement = statement.order_by(*orders)
        result = await self.db.execute(statement)
        return result.scalars().all()

    async def create(self, obj_in: CreateSchemaType) -> ModelType:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)  # type: ignore
        self.db.add(db_obj)
        await self.db.flush()
        await self.db.refresh(db_obj)
        return db_obj

    async def create_from_data(self, *, obj_in_data: dict) -> ModelType:
        db_obj = self.model(**obj_in_data)  # type: ignore
        self.db.add(db_obj)
        await self.db.flush()
        await self.db.refresh(db_obj)
        return db_obj

    async def update(
        self, db_obj: ModelType, obj_in: UpdateSchemaType | dict[str, Any]
    ) -> ModelType:
        obj_data = jsonable_encoder(db_obj)
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.model_dump(exclude_unset=True)
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        self.db.add(db_obj)
        await self.db.flush()
        await self.db.refresh(db_obj)
        return db_obj

    async def remove(self, *args: Any, **kwargs: Any):
        await self.db.execute(delete(self.model).filter(*args).filter_by(**kwargs))

    def apply_filters(self, statement: Select, filters: Filters) -> Select:
        op_map = {
            "eq": lambda x, y: x == y,
            "in": lambda x, y: x.in_(y),
            "date_eq": lambda x, y: cast(x, Date) == datetime.datetime.fromisoformat(y),
        }
        stmt = select(statement.subquery("res"))
        for flt in filters.filters:
            stmt = stmt.where(
                op_map[flt.operator](stmt.selected_columns.get(flt.property), flt.value)
            )
        return stmt
