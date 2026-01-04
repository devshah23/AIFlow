
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select,delete
from app.exceptions.Exceptions import DatabaseError, NotFoundError
from app.models.workflow_edges import WorkflowEdges, WorkflowEdgesBase
from app.repositories.base import BaseRepository
from sqlalchemy.exc import SQLAlchemyError


class WorkflowEdgeRepository(BaseRepository[WorkflowEdges]):
    def __init__(self) -> None:
        super().__init__(WorkflowEdges)
    
    async def find_edges(self,db:AsyncSession,workflow_id:int)->list[WorkflowEdges]:
        try:
            result=await db.execute(
                select(WorkflowEdges).where(WorkflowEdges.workflow_id==workflow_id)
            )
            workflow=result.scalar_one_or_none()
            
            if not workflow:
                raise NotFoundError(f"WorkflowEdges with workflow_id {workflow_id} not found")
            
            return list((await db.scalars(select(WorkflowEdges).where(WorkflowEdges.workflow_id==workflow_id))).all())
        
        except SQLAlchemyError as e:
            raise DatabaseError("Failed to fetch workflow list") from e
    
    async def delete_edges_by_workflow_id(self,db:AsyncSession,workflow_id:int):
        try:
            if not isinstance(workflow_id, int):
                raise ValueError("workflow_id must be an int")
            stmt = delete(WorkflowEdges).where(WorkflowEdges.workflow_id==workflow_id) 
            await db.execute(stmt)
        except SQLAlchemyError as e:
            raise DatabaseError("Failed to delete workflow edges") from e
            
        