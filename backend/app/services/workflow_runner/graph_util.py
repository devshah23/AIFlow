from typing import Set
from app.exceptions.Exceptions import WorkflowCycleException
from app.models.workflow_nodes import WorkflowNodes
from app.models.workflow_edges import WorkflowEdges


def build_adjacency_list(nodes: list[WorkflowNodes], edges: list[WorkflowEdges]) :
    """
    Converts workflow nodes and edges into an adjacency list.
    Node IDs are keys, values are list of downstream node IDs.
    """
    adj_list = {node.id: [] for node in nodes}
    for edge in edges:
        adj_list[edge.from_node].append(edge.to_node)
    return adj_list


def topological_sort(nodes: list[WorkflowNodes], edges: list[WorkflowEdges]) -> list[WorkflowNodes]:
    """
    Returns nodes in topologically sorted order for execution.
    """
    adj_list = build_adjacency_list(nodes, edges)
    visited: Set[int] = set()
    visiting: Set[int] = set()
    result: list[WorkflowNodes] = []

    # Map node id -> node object
    node_map = {node.id: node for node in nodes}

    def dfs(node_id:int):
        if node_id in visited:
            return
        if node_id in visiting:
            raise WorkflowCycleException(f"Cycle detected at node {node_id}")
        visiting.add(node_id)
        for neighbor in adj_list.get(node_id, []):
            dfs(neighbor)
        visiting.remove(node_id)
        visited.add(node_id)
        result.append(node_map[node_id])

    for node in nodes:
        if node.id is not None and node.id not in visited:
            dfs(node.id)

    # Reverse to get correct execution order: upstream first
    return result[::-1]


def get_start_nodes(nodes: list[WorkflowNodes], edges: list[WorkflowEdges]) -> list[WorkflowNodes]:
    """
    Returns nodes without incoming edges (starting points for execution)
    """
    all_node_ids = {node.id for node in nodes}
    target_ids = {edge.to_node for edge in edges}
    start_ids = all_node_ids - target_ids
    node_map = {node.id: node for node in nodes}
    return [node_map[node_id] for node_id in start_ids]


def get_downstream_nodes(node_id: int, edges: list[WorkflowEdges]) -> list[int]:
    """
    Returns list of downstream node IDs connected to the given node
    """
    return [edge.to_node for edge in edges if edge.from_node == node_id]

def get_upstream_nodes(node_id: int, edges: list[WorkflowEdges]) -> list[int]:
    """
    Returns list of upstream node IDs connected to the given node
    """
    return [edge.from_node for edge in edges if edge.to_node == node_id]
