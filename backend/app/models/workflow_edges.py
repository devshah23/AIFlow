from sqlalchemy import Column, ForeignKey, Integer
from sqlmodel import Field, Relationship, SQLModel
from app.models.mixin.TimestampMixin import TimestampMixin


class WorkflowEdgesBase(SQLModel):
    from_node:int=Field(nullable=False,foreign_key="workflownodes.id")
    to_node:int=Field(nullable=False,foreign_key="workflownodes.id")

class WorkflowEdges(TimestampMixin,WorkflowEdgesBase,table=True):
    id:int|None=Field(default=None,primary_key=True)
    workflow_id:int=Field(sa_column=Column(Integer,ForeignKey("workflows.id",ondelete="CASCADE"),nullable=False,index=True))

class WorkflowEdgesCreate(WorkflowEdgesBase):
    workflow_id:int|None=None

class WorkflowEdgesRead:
    id:int

class WorkflowEdgesUpdate(WorkflowEdgesBase):
    id:int


