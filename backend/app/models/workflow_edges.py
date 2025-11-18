from sqlmodel import Field, SQLModel

from app.models.mixin.TimestampMixin import TimestampMixin


class WorkflowEdgesBase(SQLModel):
    from_node:int=Field(nullable=False,foreign_key="workflownodes.id")
    to_node:int=Field(nullable=False,foreign_key="workflownodes.id")
    workflow_id:int=Field(nullable=False,index=True,foreign_key="workflows.id")

class WorkflowEdges(TimestampMixin,WorkflowEdgesBase,table=True):
    id:int|None=Field(default=None,primary_key=True)

class WorkflowEdgesCreate(WorkflowEdgesBase):
    pass

class WorkflowEdgesRead:
    id:int

class WorkflowEdgesUpdate(WorkflowEdgesBase):
    id:int