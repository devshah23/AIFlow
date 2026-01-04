from sqlite3 import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from sqlmodel import func, select

from app.exceptions.Exceptions import DatabaseError, NotFoundError, ValidationError
from app.models.chats import Chats, ChatsCreate, ChatsRead
from app.models.messages import Messages, MessagesCreate

class ChatRepository:
    def __init__(self):
        pass
    
    async def save_chat(self, db: AsyncSession, chat_data: ChatsCreate) -> Chats:
        try:
            obj=Chats(**chat_data.model_dump())
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
    
    async def get_all_chats(self, db: AsyncSession)->list[ChatsRead]:
        try:
            result = await db.execute(
                select(Chats)
            )
            chats = result.scalars().all()
            return [ChatsRead.model_validate(chat) for chat in chats]
        except SQLAlchemyError as e:
            raise DatabaseError("Database error during fetch all chats") from e   
    
    async def delete_chat(self, db: AsyncSession, chat_id: int) -> None:
        try:
            chat = await db.get(Chats, chat_id)
            if not chat:
                raise ValidationError(f"Chat with id {chat_id} not found")
            await db.delete(chat)
        except SQLAlchemyError as e:
            raise DatabaseError("Database error during delete") from e

    async def get_chat(self, db: AsyncSession, chat_id: int) -> ChatsRead:
        try:
            chat = await db.get(Chats, chat_id)
            if not chat:
                raise NotFoundError(f"Chat with id {chat_id} not found")
            return ChatsRead.model_validate(chat)
        except SQLAlchemyError as e:
            raise DatabaseError("Database error during fetch chat") from e

    async def save_messages(self, db: AsyncSession, messages: list[MessagesCreate]):
        try:
            objs = [Messages(**msg.model_dump()) for msg in messages]
            db.add_all(objs)
            await db.flush()
            return objs
        except TypeError as e:
            raise ValidationError(str(e)) from e
        except IntegrityError as e:
            raise DatabaseError("Postgres integrity error") from e
        except SQLAlchemyError as e:
            raise DatabaseError("Database error during save messages") from e

    