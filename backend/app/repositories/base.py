from typing import Generic, Type, TypeVar
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import SQLModel
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from app.exceptions.Exceptions import *

ModelType=TypeVar("ModelType",bound=SQLModel)


class BaseRepository(Generic[ModelType]):
    def __init__(self,model:Type[ModelType]) -> None:
        self.model=model
    
    async def create(self,db:AsyncSession,obj_in:dict)->ModelType:
        try:
            obj = self.model(**obj_in)
            db.add(obj)
            await db.flush()
            await db.refresh(obj)
            return obj

        except TypeError as e:
            raise ValidationError(str(e)) from e
        except IntegrityError as e:
            raise DatabaseError("Postgres integrity error") from e
        except SQLAlchemyError as e:
            raise DatabaseError("Database error during create") from e
    
    async def create_many(self, db: AsyncSession, obj_data_list: list[dict]) -> list[ModelType]:
        try:
            obj_list = [self.model(**data) for data in obj_data_list]
            db.add_all(obj_list)
            await db.flush()
            return obj_list

        except TypeError as e:
            raise ValidationError(str(e)) from e
        except IntegrityError as e:
            raise DatabaseError("Postgres integrity error on batch insert") from e
        except SQLAlchemyError as e:
            raise DatabaseError("Database error during batch insert") from e
        
    
    async def get(self,db:AsyncSession,id:int):
        try:
            obj = await db.get(self.model, id)
            if obj is None:
                raise NotFoundError(f"{self.model.__name__} with id {id} not found")
            return obj
        except SQLAlchemyError as e:
            raise DatabaseError("Database error during get") from e
    
    async def update(self, db: AsyncSession, obj_data: dict) -> ModelType | None:
        try:
            obj = await db.get(self.model, obj_data.get("id"))
            if not obj:
                raise NotFoundError(
                    f"{self.model.__name__} with id {obj_data.get('id')} not found"
                )

            for key, value in obj_data.items():
                if key not in {"id", "created_at", "updated_at"}:
                    setattr(obj, key, value)

            db.add(obj)
            return obj

        except TypeError as e:
            raise ValidationError(str(e)) from e
        except SQLAlchemyError as e:
            raise DatabaseError("Database error during update") from e

        
    async def delete(self,db:AsyncSession,obj:ModelType)->None:
        try:
            await db.delete(obj)
        except SQLAlchemyError as e:
            raise DatabaseError("Database error during delete") from e
        
        
        
        