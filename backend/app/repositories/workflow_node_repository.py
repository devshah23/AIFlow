
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select,delete
from app.models.workflow_nodes import WorkflowNodes, WorkflowNodesBase
from app.repositories.base import BaseRepository
from app.exceptions.Exceptions import DatabaseError, NotFoundError
from sqlalchemy.exc import SQLAlchemyError


class WorkflowNodeRepository(BaseRepository[WorkflowNodes]):
    def __init__(self) -> None:
        super().__init__(WorkflowNodes)
    
    async def find_nodes(self,db:AsyncSession,workflow_id:int)->list[WorkflowNodes]:
        try:
            result=await db.execute(
                select(WorkflowNodes).where(WorkflowNodes.workflow_id==workflow_id)
            )
            workflow=result.scalar_one_or_none()
            
            if not workflow:
                raise NotFoundError(f"WorkflowNodes with workflow_id {workflow_id} not found")
            
            return list((await db.scalars(select(WorkflowNodes).where(WorkflowNodes.workflow_id==workflow_id))).all())
        
        except SQLAlchemyError as e:
            raise DatabaseError("Failed to fetch workflow nodes list") from e
    
    
    async def batch_update(self,db:AsyncSession,nodes):
        from sqlalchemy import inspect
        mapper = inspect(WorkflowNodes) 
        list_of_node_dicts=[n.model_dump() for n in nodes]
        await db.run_sync(
        lambda sync_db: sync_db.bulk_update_mappings(mapper,list_of_node_dicts))
    
    async def remove_nodes_by_ids(self,db:AsyncSession,node_ids:list[int|None]):
        if not node_ids:
            return
        
        stmt=delete(WorkflowNodes).where(WorkflowNodes.id.in_(node_ids))
        await db.execute(stmt)
    
    async def remove_metadata_by_ids(self,db:AsyncSession,metadata_ids:list[int|None]):
        if not metadata_ids:
            return
        from app.models.file_metadata import FileMetadata
        stmt=delete(FileMetadata).where(FileMetadata.id.in_(metadata_ids))
        await db.execute(stmt)