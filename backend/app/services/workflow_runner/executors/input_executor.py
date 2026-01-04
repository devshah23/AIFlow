from app.exceptions.Exceptions import InvalidNodeConfigException
from app.services.workflow_runner.context import WfExecutionContext
from app.services.workflow_runner.executors.base_executor import NodeExecutor

class InputExecutor(NodeExecutor):
    
    async def execute(self, context: WfExecutionContext,upstream_nodes):
        try:
            cfg = self.node.config
            # query = cfg["query"]
            query_dict=context.get("input_query")
            if query_dict is not None:
                query=query_dict.get("output","")
            if query=="":
                raise InvalidNodeConfigException("Input query not found for running workflow")
            return {
                "output":f"Input Node Query: {query}",
            }
        
        except Exception as e:
            raise Exception(f"Input Node Executor failed") from e