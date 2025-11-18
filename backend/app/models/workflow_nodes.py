from enum import Enum
from typing import Optional
from sqlalchemy import  Column
from sqlmodel import Field, SQLModel
from sqlalchemy.dialects.postgresql import JSONB,ENUM
from app.models.mixin.TimestampMixin import TimestampMixin

class WorkflowNodesTypes(str,Enum):
    INPUTNODE="input"
    OUTPUTNODE="output"
    LLMNODE="llm"
    KNOWLEDGEBASENODE="knowledgebase"


class WorkflowNodesBase(SQLModel):
    type:WorkflowNodesTypes=Field(sa_column=Column(ENUM(WorkflowNodesTypes,name="workflownodetypes"),nullable=False))
    position:Optional[dict]=Field(default_factory=dict,sa_column=Column(JSONB))
    config:Optional[dict]=Field(default_factory=dict,sa_column=Column(JSONB))
    workflow_id:int=Field(nullable=False,index=True,foreign_key="workflows.id")

class WorkflowNodes(TimestampMixin,WorkflowNodesBase,table=True):
    id:int|None=Field(default=None,primary_key=True)

class WorkflowNodesCreate(WorkflowNodesBase):
    pass

class WorkflowNodesRead:
    id:int

class WorkflowNodesUpdate(WorkflowNodesBase):
    id:int