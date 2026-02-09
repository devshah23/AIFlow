from app.models.workflow_nodes import WorkflowNodesTypes
from app.adapters.node_convertors import *


class NodeConverterFactory:
    converters = {
        WorkflowNodesTypes.INPUTNODE: InputNodeConverter(),
        WorkflowNodesTypes.KNOWLEDGEBASENODE: KnowledgeBaseNodeConverter(),
        WorkflowNodesTypes.LLMNODE: LLMNodeConverter(),
        # WorkflowNodesTypes.OUTPUTNODE: OutputNodeConvertor(),  
    }

    @staticmethod
    def get_converter(node_type: WorkflowNodesTypes) -> NodeConverter:
        return NodeConverterFactory.converters.get(node_type,NodeConverter)
