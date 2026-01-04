from app.convertors.utils import NodeConvertorUtils


def split_nodes( nodes: list[dict], workflow_id: int):
    new_nodes_raw = [n for n in nodes if "new" in n.get("id", "")]
    old_nodes_raw = [n for n in nodes if n not in new_nodes_raw]
    
    # remove new from id of new nodes
    for node in new_nodes_raw:
        node["id"] = node["id"].replace("new", "")

    old_nodes = NodeConvertorUtils.convert_dict_nodes_to_models(
        old_nodes_raw,
        with_id=True,
        workflow_id=workflow_id,
    )

    new_nodes = NodeConvertorUtils.convert_dict_nodes_to_models(new_nodes_raw)
    for node in new_nodes:
        node.workflow_id = workflow_id

    return new_nodes, old_nodes
