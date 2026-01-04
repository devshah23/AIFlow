
from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException
from app.convertors.utils import NodeConvertorUtils
from app.dependencies.database import get_session
from app.dependencies.services import get_workflow_service
from app.exceptions.Exceptions import DatabaseError, NotFoundError
from app.models.apis.request import WorkflowUpdateRequest
from app.models.apis.response import ApiResponse
from app.models.workflows import WorkflowsCreate, WorkflowsDetailsRead, WorkflowsRead
from app.services.crud_services.workflow_service import WorkflowService
from sqlalchemy.ext.asyncio import AsyncSession

router=APIRouter(
    prefix="/workflow")

@router.post("/")
async def create_workflow(req_body:dict,background_tasks:BackgroundTasks,db:AsyncSession = Depends(get_session),workflow_service:WorkflowService=Depends(get_workflow_service)):
    try:
        workflow_nodes=NodeConvertorUtils.convert_dict_nodes_to_models(req_body.get("nodes",[]))
        workflow_data=WorkflowsCreate.model_validate({
            "name":req_body.get("name"),
            "description":req_body.get("description"),
            "config":req_body.get("config",{}),
            "nodes":workflow_nodes,
            "edges":req_body.get("edges",[])
        })
        workflow_obj = await workflow_service.create_workflow(db, workflow_data,background_tasks)
        
        return ApiResponse(
            success=True,
            message="Workflow created successfully",
            data=await NodeConvertorUtils.convert_workflow_response_format(db,WorkflowsRead.model_validate(workflow_obj))
        )
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e) or "Unexpected Error Occured."
        )
        

# Design Entire flow in a proper manner.
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
            data=await NodeConvertorUtils.convert_workflow_response_format(
                db, WorkflowsRead.model_validate(workflow)
            ),
        )

    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
      

@router.get("/all")
async def get_all_workflows(db:AsyncSession = Depends(get_session),workflow_service:WorkflowService=Depends(get_workflow_service)):
    try:
        workflows = await workflow_service.get_all(db)
        workflows_read = [WorkflowsDetailsRead.model_validate(wf) for wf in workflows]

        return ApiResponse(
            success=True,
            message="Workflows fetched successfully",
            data=workflows_read
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
        print(workflow)
        return ApiResponse(
            success=True,
            message="Workflow details fetched successfully",
            data=await NodeConvertorUtils.convert_workflow_response_format(db,WorkflowsRead.model_validate(workflow))
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