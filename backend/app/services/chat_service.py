from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select,func
from app.adapters.chat_response_adapter import ChatResponseAdapter
from app.exceptions.Exceptions import DatabaseError, NotFoundError
from app.models.chats import ChatsCreate, ChatsRead
from app.models.messages import Messages, MessagesCreate, MessagesFromTypes
from app.repositories.chat_repository import ChatRepository
from sqlalchemy.exc import SQLAlchemyError
from app.services.workflow_execution_service import WorkflowExecutionService

class ChatService:
    def __init__(self, chat_repository:ChatRepository,workflow_execution_service:WorkflowExecutionService):
        self.chat_repository = chat_repository
        self.workflow_execution_service = workflow_execution_service
    
    async def get_all_chats(self,db:AsyncSession):
        chats= await self.chat_repository.get_all_chats(db)
        return ChatResponseAdapter.to_frontend_chats(chats)
    
    async def get_chat(self,db:AsyncSession, chat_id:int):
        chat= await self.chat_repository.get_chat(db, chat_id)
        if not chat:
            raise NotFoundError(f"Chat with id {chat_id} not found")
        msg_data= await self.get_messages(db, chat_id)
        return {"chat":chat, "message_details":msg_data}
    
    
    async def create_chat(self,db:AsyncSession, chat_data:ChatsCreate):
        data= await self.chat_repository.save_chat(db, chat_data) 
        await db.commit()
        return ChatResponseAdapter.to_frontend_chats([ChatsRead.model_validate(data)])[0]
    
    async def get_messages(self, db: AsyncSession, chat_id: int, limit: int = 20, cursor: int | None = None):
        try:
            messages = await self.__fetch_messages(db, chat_id, limit, cursor)
            total = await self.__count_messages_for_chat(db, chat_id)
            
            return self.__build_paginated_response_of_messages(
                messages=messages,
                total=total,
                limit=limit
            )

        except SQLAlchemyError as e:
            raise DatabaseError("Database error during fetch messages") from e
    
    async def delete_chat(self,db:AsyncSession, chat_id: int):
        data= await self.chat_repository.delete_chat(db, chat_id)
        await db.commit()
        return data
    
    async def process_workflow_request(self,db:AsyncSession,chat_id:int, message:str):
        chat= await self.chat_repository.get_chat(db, chat_id)
        if not chat:
            raise NotFoundError(f"Chat with id {chat_id} not found")
        
        execution_result= await self.__run_workflow(db, chat.workflow_id, message)
        
        messages = await self.__persist_messages_of_execution_request(db, chat_id, message, execution_result)
        
        user_message=ChatResponseAdapter.to_frontend_message(messages[0])
        workflow_message=ChatResponseAdapter.to_frontend_message(messages[1])
        return {"user_message":user_message,"workflow_message":workflow_message}
    
    # --------------------------------------------
    # HELPER METHODS
    # --------------------------------------------
    
    async def __fetch_messages(
    self,
    db: AsyncSession,
    chat_id: int,
    limit: int,
    cursor: int | None,
) -> list[Messages]:
        stmt = (
            select(Messages)
            .where(Messages.chat_id == chat_id)
            .order_by(Messages.id.desc())
            .limit(limit))

        if cursor is not None:
            stmt = stmt.where(Messages.id < cursor)

        result = await db.execute(stmt)
        return list(result.scalars().all())

    async def __count_messages_for_chat(
    self,
    db: AsyncSession,
    chat_id: int,
    ) -> int:
        stmt = select(func.count(Messages.id)).where(Messages.chat_id == chat_id)
        result = await db.execute(stmt)
        return result.scalar() or 0
    
    def __build_paginated_response_of_messages(
    self,
    messages: list[Messages],
    total: int,
    limit: int,
    ):
        return ChatResponseAdapter.to_frontend_messages_with_pagination({
            "messages": messages,
            "next_cursor": messages[-1].id if messages else None,
            "total_messages": total,
            "has_more": len(messages) == limit,
        })

    async def __run_workflow(self,db:AsyncSession, workflow_id:int, message:str):
        execution_output= await self.workflow_execution_service.run(db, workflow_id, message)
        return execution_output.get("output","")
    
    async def __persist_messages_of_execution_request(self,db: AsyncSession,chat_id: int,user_message: str,workflow_output: str):
        messages = [
            MessagesCreate(
                chat_id=chat_id,
                from_entity=MessagesFromTypes.USER,
                content=user_message
            ),
            MessagesCreate(
                chat_id=chat_id,
                from_entity=MessagesFromTypes.WORKFLOW,
                content=workflow_output
            ),
        ]

        saved = await self.chat_repository.save_messages(db, messages)
        await db.commit()

        for msg in saved:
            await db.refresh(msg)

        return saved
