from sqlalchemy import Column
from sqlmodel import Field, SQLModel
from sqlalchemy.dialects.postgresql import JSONB,ENUM
from enum import Enum
class MessagesFromTypes(str,Enum):
    USER="user"
    WORKFLOW="workflow"

class MessagesBase(SQLModel):
    content: str=Field(default="")
    from_entity:MessagesFromTypes=Field(sa_column=Column(ENUM(MessagesFromTypes,name="Messagesfromtypes"),nullable=False))
    chat_id:int=Field(nullable=False,index=True,foreign_key="chats.id")

class Messages(MessagesBase,table=True):
    id:int|None=Field(default=None,primary_key=True)

class MessagesCreate(MessagesBase):
    pass

class MessagesRead:
    id:int

class MessagesUpdate(MessagesBase):
    id:int