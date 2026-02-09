from app.exceptions.Exceptions import InvalidWorkflowException, NotFoundException
from app.models import workflow_nodes
from app.models.workflow_nodes import WorkflowNodesTypes
from app.models.workflows import Workflows
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
        workflow = await self._load_workflow_or_fail(db, workflow_id)
        
        self._validate_workflow(workflow)

        context = self._prepare_context(user_query)
        
        execution_order = GraphUtils.topological_sort(workflow.nodes, workflow.edges)

        await self._execute_workflow(workflow, execution_order, context)
        
        output=self._extract_output(workflow, context)
        
        return {"output":output}
    
    
    
    
    # ----------------------------
    # HELPER METHODS
    # ----------------------------
    
    async def _load_workflow_or_fail(self, db: AsyncSession, workflow_id: int)->Workflows:
        workflow = await self.workflow_repo.get_entire_workflow(db, workflow_id)
        if not workflow:
            raise NotFoundException(f"Workflow {workflow_id} not found")
        return workflow
    
    def _validate_workflow(self, workflow:Workflows):
        node_types = {node.type for node in workflow.nodes}

        if WorkflowNodesTypes.INPUTNODE not in node_types:
            raise InvalidWorkflowException("Input Node Missing in Workflow")

        if WorkflowNodesTypes.OUTPUTNODE not in node_types:
            raise InvalidWorkflowException("Output Node Missing in Workflow")

    def _prepare_context(self, user_query: str) -> WfExecutionContext:
        context = WfExecutionContext()
        context.set("input_query", WorkflowNodesTypes.INPUTNODE, user_query)
        return context

    async def _execute_workflow(
        self,
        workflow,
        execution_order,
        context: WfExecutionContext):
        for node in execution_order:
            executor = self.executor_factory.get_executor(node)

            upstream_nodes = (
                GraphUtils.get_upstream_nodes(node.id, workflow.edges)
                if node.id is not None
                else []
            )

            try:
                result = await executor.execute(context, upstream_nodes)
                context.set(node.id, node.type, result)
            except Exception as e:
                raise RuntimeError(
                    f"{node.type.upper()} node failed"
                ) from e

    def _extract_output(self, workflow, context: WfExecutionContext):
        output_node = next(
            (node for node in workflow.nodes if node.type == WorkflowNodesTypes.OUTPUTNODE),
            None,
        )

        if not output_node or output_node.id is None:
            raise NotFoundException("No output node found in the workflow")

        return context.get_output(output_node.id)
