from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from app.dependencies.database import get_session
from app.dependencies.services import get_execution_service
from app.exceptions.Exceptions import InvalidWorkflowException, NotFoundException
from app.models.apis.response import ApiResponse
from app.services.workflow_execution_service import WorkflowExecutionService

router=APIRouter()

class RequestModel(BaseModel):
    query: str

@router.post("/run/{workflow_id}")
async def run_workflow(req:RequestModel,workflow_id: int,db:AsyncSession=Depends(get_session),workflow_execution_service:WorkflowExecutionService=Depends(get_execution_service)):
    try:
        response=await workflow_execution_service.run(db,workflow_id,req.query)
        return ApiResponse(
        success=True,
        data={"output": response.get("output")}
        )
    
    except RuntimeError as e:
        raise HTTPException(
            status_code=503,
            detail=str(e) or "Failed to execute the workflow"
        )
    
    except NotFoundException as e:
        raise HTTPException(
            status_code=404,
            detail=str(e) or "Not found data for execution"
        )
    
    except InvalidWorkflowException as e:
        raise HTTPException(
            status_code=400,
            detail=str(e) or "Invalid Workflow"
        )
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e) or "Unexpected Error occured"
        )

