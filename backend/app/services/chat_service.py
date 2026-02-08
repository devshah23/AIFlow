from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select,func
from app.convertors.chat_convertor_utils import ChatConvertorUtils
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
        return ChatConvertorUtils.convert_chat_response_format(chats)
    
    async def get_chat(self,db:AsyncSession, chat_id:int):
        chat= await self.chat_repository.get_chat(db, chat_id)
        if not chat:
            raise NotFoundError(f"Chat with id {chat_id} not found")
        msg_data= await self.get_messages(db, chat_id)
        return {"chat":chat, "message_details":msg_data}
    
    
    async def create_chat(self,db:AsyncSession, chat_data:ChatsCreate):
        data= await self.chat_repository.save_chat(db, chat_data) 
        await db.commit()
        chat=ChatsRead.model_validate(data)
        return ChatConvertorUtils.convert_chat_response_format([chat])[0]
    
    async def get_messages(self, db: AsyncSession, chat_id: int, limit: int = 20, cursor: int | None = None):
        try:
            query = (
                select(Messages)
                .where(Messages.chat_id == chat_id)
                .order_by(Messages.id.desc())
                .limit(limit)
            )
            
            if cursor:
                query = query.where(Messages.id < cursor)

            result = await db.execute(query)
            messages = result.scalars().all()

            
            count_stmt = select(func.count(Messages.id)).where(Messages.chat_id == chat_id)
            count_result = await db.execute(count_stmt)
            total_message_count = count_result.scalar() or 0
            
            has_more = len(messages) == limit

            messages_details= {
                "messages": list(messages),
                "next_cursor": messages[-1].id if messages else None,
                "total_messages": total_message_count,
                "has_more": has_more
            }
            return ChatConvertorUtils.convert_messages_response_format(messages_details)

        except SQLAlchemyError as e:
            raise DatabaseError("Database error during fetch messages") from e
    
    async def delete_chat(self,db:AsyncSession, chat_id: int):
        data= await self.chat_repository.delete_chat(db, chat_id)
        await db.commit()
        return data
    
    async def execute_workflow(self,db:AsyncSession,chat_id:int, message:str):
        chat= await self.chat_repository.get_chat(db, chat_id)
        if not chat:
            raise NotFoundError(f"Chat with id {chat_id} not found")
        workflow_id=chat.workflow_id
        execution_result= await self.workflow_execution_service.run(db, workflow_id, message)
        user_message=MessagesCreate(chat_id=chat_id, from_entity=MessagesFromTypes.USER, content=message)
        workflow_output_msg=MessagesCreate(chat_id=chat_id, from_entity=MessagesFromTypes.WORKFLOW, content=execution_result.get("output",""))
        messages_to_save=[user_message,workflow_output_msg]


        messages=await self.chat_repository.save_messages(db, messages_to_save)
        await db.commit()
        await db.refresh(messages[0])
        await db.refresh(messages[1])
        user_message=ChatConvertorUtils.convert_message_response_format(messages[0])
        workflow_message=ChatConvertorUtils.convert_message_response_format(messages[1])
        return {"user_message":user_message,"workflow_message":workflow_message}