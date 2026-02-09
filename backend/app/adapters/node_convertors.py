from app.adapters.node_convertor_base import NodeConverter
from app.models.workflow_nodes import WorkflowNodesBase, WorkflowNodesCreate, WorkflowNodesTypes, WorkflowNodesUpdate


class InputNodeConverter(NodeConverter):
    @staticmethod
    def convert(node,with_id:bool=False,workflow_id:int=0):
        if with_id:
            return WorkflowNodesUpdate(
                id=node.get("id"),
                workflow_id=workflow_id,
                type=WorkflowNodesTypes.INPUTNODE,
                position=node.get("position", {}),
                config={
                    "query": node["data"].get("query"),
                    "frontend_id":str(node.get("id"))
                    },
            )
        
        return WorkflowNodesCreate(
            type=WorkflowNodesTypes.INPUTNODE,
            position=node.get("position", {}),
            config={
                "query": node["data"].get("query"),
                "frontend_id":str(node.get("id"))
                },
        )


class KnowledgeBaseNodeConverter(NodeConverter):
    @staticmethod
    def convert(node,with_id:bool=False,workflow_id:int=0):
        if with_id:
            return WorkflowNodesUpdate(
                id=node.get("id"),
                workflow_id=workflow_id,
                type=WorkflowNodesTypes.KNOWLEDGEBASENODE,
                position=node.get("position", {}),
                config={
                    "metadata_id": node["data"].get("metadataId"),
                    "frontend_id":str(node.get("id"))
                    
                },
        
            )
        
        
        return WorkflowNodesCreate(
            type=WorkflowNodesTypes.KNOWLEDGEBASENODE,
            position=node.get("position", {}),
            config={
                "metadata_id": node["data"].get("metadataId"),
                "frontend_id":str(node.get("id"))
            },
        
        )


class LLMNodeConverter(NodeConverter):
    @staticmethod
    def convert( node,with_id:bool=False,workflow_id:int=0):
        if with_id:
            return WorkflowNodesUpdate(
                id=node.get("id"),
                workflow_id=workflow_id,
                type=WorkflowNodesTypes.LLMNODE,
                position=node.get("position", {}),
                config={
                    "model": node["data"].get("model"),
                    "temperature": node["data"].get("temperature"),
                    "prompt": node["data"].get("prompt"),
                    "api_key":node["data"].get("apiKey"),
                    "frontend_id":str(node.get("id"))
                },
        
            )
        
        
        
        return WorkflowNodesCreate(
            type=WorkflowNodesTypes.LLMNODE,
            position=node.get("position", {}),
            config={
                "model": node["data"].get("model"),
                "temperature": node["data"].get("temperature"),
                "prompt": node["data"].get("prompt"),
                "api_key":node["data"].get("apiKey"),
                "frontend_id":str(node.get("id"))
            },
        
        )

class OutputNodeConverter(NodeConverter):
    @staticmethod
    def convert( node,with_id:bool=False,workflow_id:int=0):
        if with_id:
            return WorkflowNodesUpdate(
                id=node.get("id"),
                workflow_id=workflow_id,
                type=WorkflowNodesTypes.OUTPUTNODE,
                position=node.get("position", {}),
                config={
                    "frontend_id":str(node.get("id"))
                }
                )
        
        
        return WorkflowNodesCreate(
            type=WorkflowNodesTypes.OUTPUTNODE,
            position=node.get("position", {}),
            config={
                "frontend_id":str(node.get("id"))
            }
        )