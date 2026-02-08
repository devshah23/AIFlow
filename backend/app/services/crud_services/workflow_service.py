from fastapi import BackgroundTasks, Depends
from pydantic import ValidationError
from sqlalchemy import delete
from app.convertors.edge_convertor import EdgeConvertor
from app.convertors.utils import NodeConvertorUtils
from app.embeddings.embedding_orchestrator import EmbeddingOrchestratorService
from app.exceptions.Exceptions import DatabaseError, NotFoundError
from app.models.apis.request import WorkflowUpdateRequest
from app.models.file_metadata import FileMetadata
from app.models.workflow_nodes import WorkflowNodes, WorkflowNodesCreate, WorkflowNodesTypes
from app.models.workflows import Workflows, WorkflowsCreate, WorkflowsDetailsRead, WorkflowsRead, WorkflowsUpdate
from app.repositories.workflow_edge_repository import WorkflowEdgeRepository
from app.repositories.workflow_node_repository import WorkflowNodeRepository
from app.repositories.workflow_repository import WorkflowRepository
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from app.services.crud_services.helper import split_nodes


class WorkflowService:
    """
    Service for managing workflows.
    """

    def __init__(self,workflow_repo:WorkflowRepository,workflow_node_repo:WorkflowNodeRepository,workflow_edge_repo:WorkflowEdgeRepository):
        self.workflow_repo=workflow_repo
        self.workflow_node_repo=workflow_node_repo
        self.workflow_edge_repo=workflow_edge_repo
    
    async def create_workflow(self, db, workflow_data: WorkflowsCreate,background_tasks:BackgroundTasks):
        try:
            async with db.begin():
                workflow_obj = await self.workflow_repo.create(
                    db, workflow_data.model_dump(exclude={"nodes", "edges"})
                )

                if not workflow_obj:
                    raise DatabaseError("Failed to create workflow")

                
                nodes_in_db = []
                if workflow_data.nodes:
                    nodes = [
                        n.model_copy(update={"workflow_id": workflow_obj.id}).model_dump()
                        for n in workflow_data.nodes
                    ]
                    nodes_in_db = await self.workflow_node_repo.create_many(db, nodes)
                
                kb_nodes = [
                    node for node in nodes_in_db
                    if node.type == WorkflowNodesTypes.KNOWLEDGEBASENODE
                ]

                # UPDATE FileMetadata created using FILE UPLOAD APIs with workflow_id and node_id for knowledge base nodes.
                metadata_ids = [
                    node.config.get("metadata_id")
                    for node in kb_nodes
                    if node.config.get("metadata_id") is not None
                ]

                if metadata_ids:
                    stmt = select(FileMetadata).where(FileMetadata.id.in_(metadata_ids))
                    result = await db.execute(stmt)
                    file_metadatas = result.scalars().all()                    
                    metadata_map = {fm.id: fm for fm in file_metadatas}

                    for node in kb_nodes:
                        metadata_id = node.config.get("metadata_id")
                        fm = metadata_map.get(metadata_id)
                        if fm:
                            fm.node_id = node.id
                            fm.workflow_id = workflow_obj.id
                            embedding_service=EmbeddingOrchestratorService()
                            background_tasks.add_task(embedding_service.generate_store_embeddings,
                                                    fm.file_type,
                                                    fm.file_name,
                                                    fm.id,background_tasks)
                await db.refresh(workflow_obj,attribute_names=["nodes","edges"])
                if workflow_data.edges:
                    edges=EdgeConvertor.convert_to_edge_format( [
                        {"id": x.id, "frontend_id": x.config.get("frontend_id")}for x in nodes_in_db
                        ],workflow_data.edges)
                    
                    edges=[
                        e.model_copy(update={"workflow_id": workflow_obj.id}).model_dump()
                        for e in edges
                    ]
                    
                    await self.workflow_edge_repo.create_many(db, edges)

            await db.refresh(workflow_obj,attribute_names=["nodes","edges"])
            return await NodeConvertorUtils.convert_workflow_response_format(db,WorkflowsRead.model_validate(workflow_obj))

        except DatabaseError as e:
            raise DatabaseError("Failed to create workflow") from e
        except ValidationError as e:
            raise ValidationError("Invalid data for creating workflow"+str(e)) from e
    
    
    async def update_workflow( self,
    db: AsyncSession,
    workflow_id: int,
    req: WorkflowUpdateRequest,
    background_tasks: BackgroundTasks,):
        workflow_db_obj = await self.get_entire_workflow(db, workflow_id)
        if not workflow_db_obj:
            raise NotFoundError(f"Workflow with id {workflow_id} does not exist")

        req_nodes_id=[int(n.get("id",0)) for n in req.nodes if "new" not in n.get("id","") and int(n.get("id",0)) != 0]
        
        # Delete already existing edges of workflow
        await self.remove_all_edges_of_workflow(db, workflow_id)      
        
        # Delete nodes and their metadatas which are removed from workflow  
        deleted_nodes=[n for n in workflow_db_obj.nodes if n.id not in req_nodes_id]
        await self.remove_nodes_by_ids(db, deleted_nodes)

        await db.refresh(workflow_db_obj,attribute_names=["nodes","edges"])

        new_nodes, old_nodes = split_nodes(req.nodes, workflow_id)
        await self.workflow_node_repo.create_many(db,[n.model_dump()for n in new_nodes])
        
        old_metadata_ids = [
            int(node.config.get("metadata_id",0)) for node in workflow_db_obj.nodes
            if node.type == WorkflowNodesTypes.KNOWLEDGEBASENODE and node.config.get("metadata_id") is not None
        ]
        
        if old_metadata_ids:
            embed_service=EmbeddingOrchestratorService()
            rows=await embed_service.delete_embeddings_by_metadata_ids(old_metadata_ids)
            
            
        
        await self.workflow_node_repo.batch_update(db, old_nodes)
        
        await db.refresh(workflow_db_obj,attribute_names=["nodes","edges"])
        
        kb_nodes = [
                    node for node in workflow_db_obj.nodes
                    if node.type == WorkflowNodesTypes.KNOWLEDGEBASENODE
                ]


        metadata_ids = [
            int(node.config.get("metadata_id",0))
            for node in kb_nodes
            if node.config.get("metadata_id") is not None
        ]

        if metadata_ids:
            stmt = select(FileMetadata).where(FileMetadata.id.in_(metadata_ids))
            result = await db.execute(stmt)
            file_metadatas = result.scalars().all()                    
            metadata_map = {fm.id: fm for fm in file_metadatas}

            for node in kb_nodes:
                metadata_id = int(node.config.get("metadata_id",0))
                fm = metadata_map.get(metadata_id)
                if fm:
                    fm.node_id = node.id
                    fm.workflow_id = workflow_db_obj.id
                    embedding_service=EmbeddingOrchestratorService()
                    background_tasks.add_task(embedding_service.generate_store_embeddings,
                                            fm.file_type,
                                            fm.file_name,
                                            fm.id,background_tasks)
        await db.refresh(workflow_db_obj,attribute_names=["nodes","edges"])
        if req.edges:
            
            modified_edges=[
                {"id": x.get("id"), "source": str(x.get("source", "")).replace("new",""), "target": str(x.get("target", "")).replace("new","")}for x in req.edges
                ]
            # remove new from frontend ids
            edges=EdgeConvertor.convert_to_edge_format( [
                {"id": x.id, "frontend_id": str(x.config.get("frontend_id", "")).replace("new","")}for x in workflow_db_obj.nodes
                ],modified_edges)
            
            edges=[
                e.model_copy(update={"workflow_id": workflow_db_obj.id}).model_dump()
                for e in edges
            ]
            
            await self.workflow_edge_repo.create_many(db, edges)
        await db.commit()
        await db.refresh(workflow_db_obj,attribute_names=["nodes","edges"])
        return await NodeConvertorUtils.convert_workflow_response_format(
                db, WorkflowsRead.model_validate(workflow_db_obj)
        )


        
    
    async def get_all(self,db:AsyncSession):
        try:
            workflows = await self.workflow_repo.get_all(db)
            return [WorkflowsDetailsRead.model_validate(wf) for wf in workflows]
        except DatabaseError as e:
            raise DatabaseError("Failed to get all workflows") from e
    
    
    async def get_workflow_details(self,db:AsyncSession,workflow_id:int):
        try:
            workflow = await self.workflow_repo.get(db, workflow_id)
            
            if not workflow:
                raise NotFoundError(f"Workflow {workflow_id} not found")
            
            return workflow

        except DatabaseError as e:
            raise DatabaseError("Failed to get workflow details") from e
    
    async def get_entire_workflow(self,db:AsyncSession,workflow_id:int):
        try:
            workflow = await self.workflow_repo.get_entire_workflow(db, workflow_id)
            
            if not workflow:
                raise NotFoundError(f"Workflow {workflow_id} not found")
            
            return await NodeConvertorUtils.convert_workflow_response_format(db,WorkflowsRead.model_validate(workflow))

        except DatabaseError as e:
            raise DatabaseError("Failed to get entire workflow") from e
    
    async def delete_workflow(self,db:AsyncSession,workflow_id:int):
        try:
            workflow =  await self.workflow_repo.get(db, workflow_id)
            if not workflow:
                raise NotFoundError(f"Workflow {workflow_id} not found")
            
            metadatas=await  db.scalars(select(FileMetadata.id).where(FileMetadata.workflow_id==workflow_id))
            metadata_ids_list=metadatas.all()
            embedding_service=EmbeddingOrchestratorService()
            result=await embedding_service.delete_embeddings_by_metadata_ids(list(metadata_ids_list))
            if not result:
                raise DatabaseError("Failed to delete embeddings for workflow files")
            
            await db.execute(delete(FileMetadata).where(FileMetadata.workflow_id==workflow_id))
            await self.workflow_repo.delete(db, workflow)
            await db.commit()

        except DatabaseError as e:
            raise DatabaseError(str(e) or "Failed to delete workflow") from e
        
        
    async def save_complete_workflow_with_edges(self,db:AsyncSession,workflow:Workflows):
        try:
            await db.commit()
            await db.refresh(workflow)
            return workflow
        except:
            raise Exception("Something went wrong when creating Edges of workflow")
            
    async def remove_all_edges_of_workflow(self,db:AsyncSession,workflow_id:int):
        try:
            await self.workflow_edge_repo.delete_edges_by_workflow_id(db, workflow_id)
        except DatabaseError as e:
            raise DatabaseError("Failed to delete workflow edges while updating") from e 
        except ValueError as e:
            raise ValueError("Invalid workflow_id provided for deleting edges") from e
    
    async def remove_nodes_by_ids(self,db:AsyncSession,nodes:list[WorkflowNodes]):
        try:
            node_ids=[n.id for n in nodes]
            kb_nodes=[
                node for node in nodes
                if node.type == WorkflowNodesTypes.KNOWLEDGEBASENODE
            ]
            metadata_ids = [
                node.config.get("metadata_id")
                for node in kb_nodes
                if node.config.get("metadata_id") is not None
            ]
            embedding_service=EmbeddingOrchestratorService()
            result=await embedding_service.delete_embeddings_by_metadata_ids(metadata_ids)
            if not result:
                raise DatabaseError("Failed to delete embeddings for workflow files")
            
            await self.workflow_node_repo.remove_metadata_by_ids(db, metadata_ids)
            await self.workflow_node_repo.remove_nodes_by_ids(db, node_ids)
        except DatabaseError as e:
            raise DatabaseError("Failed to delete workflow nodes while updating") from e
        
             
            