
from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException
from app.dependencies.database import get_session
from app.dependencies.services import get_workflow_service
from app.exceptions.Exceptions import DatabaseError, NotFoundError
from app.models.apis.request import WorkflowCreateRequest, WorkflowUpdateRequest
from app.models.apis.response import ApiResponse
from app.models.workflows import WorkflowsCreate
from app.services.crud_services.workflow_service import WorkflowService
from sqlalchemy.ext.asyncio import AsyncSession

router=APIRouter(
    prefix="/workflow")

@router.post("/")
async def create_workflow(req:WorkflowCreateRequest,background_tasks:BackgroundTasks,db:AsyncSession = Depends(get_session),workflow_service:WorkflowService=Depends(get_workflow_service)):
    try:
        
        workflow_data=WorkflowsCreate.model_validate(req.model_dump())
        workflow = await workflow_service.create_workflow(db, workflow_data,background_tasks)
        
        return ApiResponse(
            success=True,
            message="Workflow created successfully",
            data=workflow
        )
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e) or "Unexpected Error Occured."
        )
        
@router.put("/{workflow_id}")
async def update_workflow(
    workflow_id: int,
    req: WorkflowUpdateRequest,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_session),
    workflow_service: WorkflowService = Depends(get_workflow_service),
):
    try:
        workflow = await workflow_service.update_workflow(
            db=db,
            workflow_id=workflow_id,
            req=req,
            background_tasks=background_tasks,
        )

        return ApiResponse(
            success=True,
            message="Workflow updated successfully",
            data=workflow
        )

    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
      
@router.get("/all")
async def get_all_workflows(db:AsyncSession = Depends(get_session),workflow_service:WorkflowService=Depends(get_workflow_service)):
    try:
        workflows = await workflow_service.get_all(db)
        return ApiResponse(
            success=True,
            message="Workflows fetched successfully",
            data=workflows
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e) or "Unexpected Error Occured."
        )

@router.get("/{workflow_id}")
async def get_workflow_details(workflow_id:int,db:AsyncSession = Depends(get_session),workflow_service:WorkflowService=Depends(get_workflow_service)):
    try:
        workflow = await workflow_service.get_entire_workflow(db, workflow_id)
        return ApiResponse(
            success=True,
            message="Workflow details fetched successfully",
            data=workflow
        )

    except DatabaseError as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
    
    except NotFoundError as e:
        raise HTTPException(
            status_code=404,
            detail=str(e)
        )
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e) or "Unexpected Error Occured."
        )

@router.delete("/{workflow_id}")
async def delete_workflow(workflow_id:int,db:AsyncSession = Depends(get_session),
                            workflow_service:WorkflowService=Depends(get_workflow_service)):
        try:
            await workflow_service.delete_workflow(db, workflow_id)
            return ApiResponse(
                success=True,
                message="Workflow deleted successfully",
                data=None
            )
    
        except DatabaseError as e:
            raise HTTPException(
            status_code=500,
            detail=str(e) or "Unexpected Error Occured."
        )
        
        except NotFoundError as e:
            raise HTTPException(
            status_code=404,
            detail=str(e) or "Not Found."
        )
        
        except Exception as e:
            raise HTTPException(
            status_code=500,
            detail=str(e) or "Unexpected Error Occured."
        )