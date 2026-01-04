from fastapi import APIRouter

from app.services.crud_services.workflow_service import WorkflowService

router=APIRouter(
    prefix="/workflow",
    tags=["workflow"]
)

@router.get("/all")
async def get_all_workflows():
    return 0

