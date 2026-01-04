from typing import  Optional
from sqlalchemy.dialects.postgresql import JSONB

from sqlalchemy import  Column
from sqlmodel import Field, Relationship, SQLModel

from app.models.mixin.TimestampMixin import TimestampMixin
from app.models.workflow_nodes import WorkflowNodesCreate, WorkflowNodesUpdate, WorkflowNodes
from app.models.workflow_edges import WorkflowEdges, WorkflowEdgesBase, WorkflowEdgesCreate


class WorkflowsBase(SQLModel):
    name:str=Field(nullable=False)
    description:Optional[str]=Field(default=None)
    config:Optional[dict]=Field(default_factory=dict,sa_column=Column(JSONB))

class Workflows(TimestampMixin,WorkflowsBase,table=True):
    id:int|None=Field(default=None,primary_key=True)
    
    nodes:list["WorkflowNodes"]=Relationship(sa_relationship_kwargs={"cascade":"all, delete-orphan"})
    edges:list["WorkflowEdges"]=Relationship(sa_relationship_kwargs={"cascade":"all, delete-orphan"})
    
Workflows.model_rebuild()
class WorkflowsCreate(WorkflowsBase):
    nodes:list["WorkflowNodesCreate"]|None
    edges:list[dict]|None

class WorkflowsRead(WorkflowsBase):
    id:int
    nodes:list["WorkflowNodes"] =[]
    edges:list["WorkflowEdges"] =[]
        
    class Config:
        from_attributes = True

class WorkflowsDetailsRead(WorkflowsBase):
    id:int

class WorkflowsUpdate(WorkflowsBase):
    id:int
    nodes:list["WorkflowNodesUpdate"]|None
    edges:list["WorkflowEdgesCreate"]|None


