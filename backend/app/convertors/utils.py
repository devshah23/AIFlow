from app.models.workflow_edges import WorkflowEdges
from app.models.workflow_nodes import WorkflowNodes, WorkflowNodesCreate, WorkflowNodesUpdate
from app.services.crud_services.uploads.kb_file_upload import get_uploaded_file_metadata
from .node_convertors import (
    InputNodeConverter,
    KnowledgeBaseNodeConverter,
    OutputNodeConverter,
    LLMNodeConverter,
    WorkflowNodesTypes)
from app.models.workflows import WorkflowsRead
from sqlalchemy.ext.asyncio import AsyncSession

class NodeConvertorUtils:
    @staticmethod
    def convert_dict_nodes_to_models(node_dicts: list,with_id:bool=False,workflow_id:int|None=None)->list[WorkflowNodesUpdate] | list[WorkflowNodesCreate]:
        node_models = []
        for node in node_dicts:
            kwargs = {"node": node, "with_id": with_id}

            if isinstance(workflow_id, int):
                kwargs["workflow_id"] = workflow_id 
            node_type = node.get("type")
            if node_type ==WorkflowNodesTypes.INPUTNODE:
                node_models.append(InputNodeConverter.convert(**kwargs ))
            elif node_type == WorkflowNodesTypes.KNOWLEDGEBASENODE:
                node_models.append(KnowledgeBaseNodeConverter.convert(**kwargs))
            elif node_type == WorkflowNodesTypes.OUTPUTNODE:
                node_models.append(OutputNodeConverter.convert(**kwargs))
            elif node_type == WorkflowNodesTypes.LLMNODE:
                node_models.append(LLMNodeConverter.convert(**kwargs))
            else:
                raise ValueError(f"Unknown node type: {node_type}")
        return node_models
    
    
    @staticmethod
    async def fill_kb_nodes_with_file_details(db:AsyncSession,workflow_obj:WorkflowsRead):
        workflow_obj.nodes=await get_uploaded_file_metadata(db,workflow_obj.nodes)
        return workflow_obj

    @staticmethod
    async def convert_workflow_response_format(db:AsyncSession,workflow_obj:WorkflowsRead)->dict:
        try:
            workflow_obj=await NodeConvertorUtils.fill_kb_nodes_with_file_details(db,workflow_obj)
            return {
            "id":workflow_obj.id,
            "name":workflow_obj.name,
            "description":workflow_obj.description,
            # "config":workflow_obj.config,
            "nodes":NodeConvertorUtils.convert_nodes_response_format(workflow_obj.nodes),
            "edges":NodeConvertorUtils.convert_edges_response_format(workflow_obj.edges),
            }
        except Exception as e:
            raise e
    @staticmethod
    def convert_nodes_response_format(nodes:list[WorkflowNodes])->list[dict]:
        converted_nodes=[]
        for node in nodes:
            node_dict=node.model_dump()
            node_dict["data"]=node_dict.pop("config",{})
            node_dict["id"]=str(node_dict["id"])
            if "frontend_id" in node_dict["data"]:
                node_dict["data"].pop("frontend_id")
            if "workflow_id" in node_dict["data"]:
                node_dict["data"].pop("workflow_id")
            if "node_id" in node_dict["data"]:
                node_dict["data"].pop("node_id")
            if "api_key" in node_dict["data"]:
                node_dict["data"]["apiKey"]=node_dict["data"].pop("api_key")
            if "file_name" in node_dict["data"]:
                node_dict["data"]["fileName"]=node_dict["data"].pop("file_name")
            if "metadata_id" in node_dict["data"]:
                node_dict["data"]["metadataId"]=node_dict["data"].pop("metadata_id")
            
            node_dict.pop("created_at",None)
            node_dict.pop("updated_at",None)
            node_dict.pop("workflow_id",None)
            converted_nodes.append(node_dict)
        return converted_nodes
    @staticmethod
    def convert_edges_response_format(edges:list[WorkflowEdges])->list[dict]:
        converted_edges=[]
        for edge in edges:
            edge_dict=edge.model_dump()
            edge_dict["id"]=str(edge_dict["id"])
            edge_dict["source"]=str(edge_dict.pop("from_node"))
            edge_dict["target"]=str(edge_dict.pop("to_node"))
            edge_dict.pop("created_at",None)
            edge_dict.pop("updated_at",None)
            converted_edges.append(edge_dict)
        return converted_edges

