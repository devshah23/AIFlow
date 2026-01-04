from __future__ import annotations


from enum import Enum
from sqlmodel.main import SQLModelConfig
from typing import Optional
from pydantic import ConfigDict
from sqlalchemy import  Column, ForeignKey, Integer
from sqlmodel import Field, Relationship, SQLModel
from sqlalchemy.dialects.postgresql import JSONB,ENUM
from app.models.mixin.TimestampMixin import TimestampMixin


class WorkflowNodesTypes(str,Enum):
    INPUTNODE="input"
    OUTPUTNODE="output"
    LLMNODE="llm"
    KNOWLEDGEBASENODE="knowledgeBase"


class WorkflowNodesBase(SQLModel):
    type:WorkflowNodesTypes=Field(sa_column=Column(ENUM(WorkflowNodesTypes,name="workflownodetypes"),nullable=False))
    position:Optional[dict]=Field(default_factory=dict,sa_column=Column(JSONB))
    config:Optional[dict]=Field(default_factory=dict,sa_column=Column(JSONB))

class WorkflowNodes(TimestampMixin,WorkflowNodesBase,table=True):
    id:int|None=Field(default=None,primary_key=True)
    workflow_id:int=Field(sa_column=Column(Integer,ForeignKey("workflows.id",ondelete="CASCADE"),nullable=False,index=True))

class WorkflowNodesCreate(WorkflowNodesBase):
    workflow_id:int|None=None

class WorkflowNodesRead:
    id:int

class WorkflowNodesUpdate(WorkflowNodesBase):
    id:int
    workflow_id:int
    
    
