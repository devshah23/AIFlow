from typing import Any, Dict,List
from pydantic import BaseModel, Field,field_validator

from app.adapters.utils import NodeConvertorUtils


class WorkflowUpdateRequest(BaseModel):
    name: str
    description: str = ""
    config: dict = {}
    nodes: list[dict] = []
    edges: list[dict] = []

class WorkflowCreateRequest(BaseModel):
    name: str
    description: str | None = None
    config: Dict[str, Any] = Field(default_factory=dict)
    nodes: List[Any] = Field(default_factory=list)
    edges: List[Dict] = Field(default_factory=list)

    @field_validator("nodes", mode="before")
    @classmethod
    def convert_nodes(cls, v):
        if v is None:
            return []
        return NodeConvertorUtils.convert_dict_nodes_to_models(v)

class CreateChatRequest(BaseModel):
    name: str = Field(default="")
    workflowId: int = Field(default=0)
    description: str = Field(default="")