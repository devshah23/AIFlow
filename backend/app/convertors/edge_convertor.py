
from app.models.workflow_edges import  WorkflowEdges, WorkflowEdgesCreate

class EdgeConvertor:
    @staticmethod
    def convert_to_edge_format(node_list:list[dict],edge_list)->list[WorkflowEdgesCreate]:
        try:
            edge_response_list=[]
            for edge in edge_list:
                edge=WorkflowEdgesCreate.model_validate({
                    "from_node":next((int(node.get("id",0)) for node in node_list if node.get("frontend_id")==edge.get("source")),None),
                    "to_node":next((int(node.get("id",0)) for node in node_list if node.get("frontend_id")==edge.get("target")),None),
                    "workflow_id":None
                })
                
                edge_response_list.append(edge)
            return edge_response_list
        except Exception as e:
            raise e
    @staticmethod
    def convert_to_edge_format_updated_nodes(node_list:list[dict],edge_list)->list[WorkflowEdgesCreate]:
        try:
            edge_response_list=[]
            for edge in edge_list:
                edge=WorkflowEdgesCreate.model_validate({
                    "from_node":next((int(node.get("id",0)) for node in node_list if str(node.get("id"))==edge.get("source")),None),
                    "to_node":next((int(node.get("id",0)) for node in node_list if str(node.get("id"))==edge.get("target")),None),
                    "workflow_id":None
                })
                
                edge_response_list.append(edge)
            return edge_response_list
        except Exception as e:
            raise e