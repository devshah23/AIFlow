from app.models.workflow_nodes import WorkflowNodesBase, WorkflowNodesTypes
from app.services.workflow_runner.context import WfExecutionContext
from app.services.workflow_runner.executors.base_executor import NodeExecutor
from app.services.workflow_runner.executors.executor_util import ExecutorUtil


class OutputExecutor(NodeExecutor):
    
    async def execute(self, context: WfExecutionContext,upstream_nodes):
        output="  \n".join(ExecutorUtil.get_data_from_upstream(context, upstream_nodes))

        return {
            "output": output
        }