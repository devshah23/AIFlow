
from app.services.workflow_runner.context import WfExecutionContext


class ExecutorUtil:
    @staticmethod
    def get_data_from_upstream(context: WfExecutionContext, upstream_nodes:list[int]):
        result=[]
        for node_id in upstream_nodes:
            result.append(context.get_output(node_id))
        return result
    @staticmethod
    def get_data_from_upstream_with_node_types(context: WfExecutionContext, upstream_nodes: list[int]):
        result = []
        for node_id in upstream_nodes:
            data = context.get_output_with_node_type(node_id)
            result.append(data)
        return result