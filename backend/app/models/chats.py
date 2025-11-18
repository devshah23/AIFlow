from sqlmodel import Field, Relationship, SQLModel

from app.models.messages import Messages


class ChatsBase(SQLModel):
    name:str =Field(default="",max_length=100)
    description:str =Field(default="",max_length=255)
    workflow_id:int=Field(nullable=False,index=True,foreign_key="workflows.id")

class Chats(ChatsBase,table=True):
    id:int|None=Field(default=None,primary_key=True)
    messages:list[Messages]=Relationship()

class ChatsCreate(ChatsBase):
    pass

class ChatsRead:
    id:int

class ChatsUpdate(ChatsBase):
    id:int