from typing import  Optional
from sqlalchemy.dialects.postgresql import JSONB

from sqlalchemy import  Column
from sqlmodel import Field, Relationship, SQLModel
from app.models.workflow_edges import WorkflowEdges
from app.models.mixin.TimestampMixin import TimestampMixin
from app.models.workflow_nodes import WorkflowNodes


class WorkflowsBase(SQLModel):
    name:str=Field(nullable=False)
    description:Optional[str]=Field(default=None)
    config:Optional[dict]=Field(default_factory=dict,sa_column=Column(JSONB))

class Workflows(TimestampMixin,WorkflowsBase,table=True):
    id:int|None=Field(default=None,primary_key=True)
    
    nodes:list[WorkflowNodes]=Relationship()
    edges:list[WorkflowEdges]=Relationship()
    
    
class WorkflowsCreate(WorkflowsBase):
    pass

class WorkflowsRead:
    id:int

class WorkflowsUpdate(WorkflowsBase):
    id:int