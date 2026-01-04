from sqlalchemy import Column, ForeignKey, Integer
from sqlmodel import Field, Relationship, SQLModel

from app.models.messages import Messages


class ChatsBase(SQLModel):
    name:str =Field(default="",max_length=100)
    description:str =Field(default="",max_length=255)
    workflow_id:int=Field(sa_column=Column(Integer,ForeignKey("workflows.id",ondelete="CASCADE"),nullable=False,index=True))

class Chats(ChatsBase,table=True):
    id:int|None=Field(default=None,primary_key=True)
    messages:list[Messages]=Relationship(sa_relationship_kwargs={"cascade":"all, delete-orphan"})

class ChatsCreate(ChatsBase):
    pass

class ChatsRead(ChatsBase):
    id:int

class ChatsUpdate(ChatsBase):
    id:int