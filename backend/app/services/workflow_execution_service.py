from app.exceptions.Exceptions import InvalidWorkflowException, NotFoundException
from app.models import workflow_nodes
from app.models.workflow_nodes import WorkflowNodesTypes
from app.repositories.workflow_edge_repository import WorkflowEdgeRepository
from app.repositories.workflow_node_repository import WorkflowNodeRepository
from app.repositories.workflow_repository import WorkflowRepository
from sqlalchemy.ext.asyncio import AsyncSession

from app.services.workflow_runner.context import WfExecutionContext
from app.services.workflow_runner import graph_util as GraphUtils
from app.services.workflow_runner.node_executor_factory import NodeExecutorFactory


class WorkflowExecutionService:
    """
    Main service to run a workflow.
    Loads workflow, manages execution context, and runs each node in order.
    """

    def __init__(
        self,
        workflow_repo: WorkflowRepository,
        node_repo: WorkflowNodeRepository,
        edge_repo: WorkflowEdgeRepository,
    ):
        self.workflow_repo = workflow_repo
        self.node_repo = node_repo
        self.edge_repo = edge_repo
        self.executor_factory = NodeExecutorFactory()

    async def run(self, db: AsyncSession, workflow_id: int,user_query:str) -> dict:
        """
        Run a workflow by ID.
        Returns dict containing output.
        """

        # Load the workflow with nodes and edges
        workflow = await self.workflow_repo.get_entire_workflow(db, workflow_id)
        if not workflow:
            raise NotFoundException(f"Workflow {workflow_id} not found")
        
        # Validation Rules
        is_input_node_in_wf=[w.id for w in workflow.nodes if w.type==WorkflowNodesTypes.INPUTNODE]
        is_output_node_in_wf=[w.id for w in workflow.nodes if w.type==WorkflowNodesTypes.OUTPUTNODE]
        if not is_input_node_in_wf:
            raise InvalidWorkflowException("Input Node Missing in Workflow")
        
        if not is_output_node_in_wf:
            raise InvalidWorkflowException("Output Node Missing in Workflow")


        # Prepare execution context
        context = WfExecutionContext()
        
        context.set("input_query",WorkflowNodesTypes.INPUTNODE, user_query)
        
        # Determine execution order (topological sort)
        execution_order = GraphUtils.topological_sort(workflow.nodes, workflow.edges)

        for node in execution_order:
            executor = self.executor_factory.get_executor(node)
            if node.id is not None:
                upstream_nodes=GraphUtils.get_upstream_nodes(node.id,workflow.edges)
            try:
                result = await executor.execute(context,upstream_nodes)
                context.set(node.id,node.type, result)
            except Exception as e:
                raise RuntimeError(f"{node.type.upper()} node failed: {e}") from e
        
        # Find and return the final output node
        output_node_id=None
        for node in workflow.nodes:
            if node.type==WorkflowNodesTypes.OUTPUTNODE:
                output_node_id=node.id
                break
        if not output_node_id:
            raise NotFoundException("No output node found in the workflow")
        output=context.get_output(output_node_id)
        
        return {"output":output}