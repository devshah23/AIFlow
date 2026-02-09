from app.models.workflow_edges import WorkflowEdgesCreate

FROM_NODE_KEY="from_node"
TO_NODE_KEY="to_node"

class EdgeAdapter:
    @staticmethod
    def _map_edges_with_node_ids(node_list:list[dict],edges_list)->list[WorkflowEdgesCreate]:
        edges_with_node_id_list=[]
        for edge in edges_list:
            edge=WorkflowEdgesCreate.model_validate({
                FROM_NODE_KEY:next((int(node.get("id",0)) for node in node_list if node.get("frontend_id")==edge.get("source")),None),
                TO_NODE_KEY:next((int(node.get("id",0)) for node in node_list if node.get("frontend_id")==edge.get("target")),None)
            })
            
            edges_with_node_id_list.append(edge)
        return edges_with_node_id_list
        
    @staticmethod
    def _attach_workflow_id(
    edges: list[WorkflowEdgesCreate],
    workflow_id: int
    ) -> list[WorkflowEdgesCreate]:
        return [
        edge.model_copy(update={"workflow_id": workflow_id})
        for edge in edges
        ]
    
    @staticmethod
    def build_edges(
        node_list: list[dict],
        edges_list,
        workflow_id: int
    ) -> list[WorkflowEdgesCreate]:
        edges = EdgeAdapter._map_edges_with_node_ids(node_list, edges_list)
        return EdgeAdapter._attach_workflow_id(edges, workflow_id)
