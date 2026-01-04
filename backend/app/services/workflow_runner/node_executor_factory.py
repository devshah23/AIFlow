from app.models.workflow_nodes import WorkflowNodesTypes
from app.services.workflow_runner.executors.input_executor import InputExecutor
from app.services.workflow_runner.executors.kb_executor import KBExecutor
from app.services.workflow_runner.executors.llm_executor import LLMExecutor
from app.services.workflow_runner.executors.output_executor import OutputExecutor


class NodeExecutorFactory:
    def __init__(self):
        self.registry = {
            WorkflowNodesTypes.LLMNODE: LLMExecutor,
            WorkflowNodesTypes.KNOWLEDGEBASENODE: KBExecutor,
            WorkflowNodesTypes.INPUTNODE: InputExecutor,
            WorkflowNodesTypes.OUTPUTNODE: OutputExecutor,
        }

    def get_executor(self, node)->LLMExecutor|KBExecutor|InputExecutor|OutputExecutor:
        node_type = node.type
        executor_cls = self.registry.get(node_type)

        if not executor_cls:
            raise ValueError(f"Unknown node type {node_type}")

        return executor_cls(node)
