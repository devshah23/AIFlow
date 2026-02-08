from fastapi import Depends
from app.dependencies.repositories import get_chat_repository, get_workflow_edge_repo, get_workflow_node_repo, get_workflow_repo
from app.services.chat_service import ChatService
from app.services.crud_services.workflow_service import WorkflowService
from app.services.workflow_execution_service import WorkflowExecutionService


async def get_workflow_service(
    workflow_repo = Depends(get_workflow_repo),workflow_node_repo=Depends(get_workflow_node_repo),workflow_edge_repo=Depends(get_workflow_edge_repo))->WorkflowService:
    return WorkflowService(workflow_repo,workflow_node_repo,workflow_edge_repo)
    

async def get_execution_service(
    workflow_repo = Depends(get_workflow_repo),workflow_node_repo=Depends(get_workflow_node_repo),workflow_edge_repo=Depends(get_workflow_edge_repo) )->WorkflowExecutionService:
    return WorkflowExecutionService(workflow_repo,workflow_node_repo,workflow_edge_repo)


async def get_chat_service(
    chat_repository = Depends(get_chat_repository),
    workflow_execution_service = Depends(get_execution_service)
)->ChatService:
    return ChatService(chat_repository, workflow_execution_service)