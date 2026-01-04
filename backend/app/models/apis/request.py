from pydantic import BaseModel


class WorkflowUpdateRequest(BaseModel):
    name: str
    description: str = ""
    config: dict = {}
    nodes: list[dict] = []
    edges: list[dict] = []
