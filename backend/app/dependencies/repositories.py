from fastapi import Depends
from app.repositories.workflow_repository import WorkflowRepository
from app.repositories.workflow_node_repository import WorkflowNodeRepository
from app.repositories.workflow_edge_repository import WorkflowEdgeRepository
from app.repositories.chat_repository import ChatRepository

async def get_workflow_repo() -> WorkflowRepository:
    return WorkflowRepository()

async def get_workflow_node_repo() -> WorkflowNodeRepository:
    return WorkflowNodeRepository()

async def get_workflow_edge_repo() -> WorkflowEdgeRepository:
    return WorkflowEdgeRepository()

async def get_chat_repository():
    return ChatRepository()