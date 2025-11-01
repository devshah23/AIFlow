import SidebarLayout from "@/components/layouts/SidebarLayout";
import CreateFlowSidebar from "@/components/sidebars/CreateFlowSidebar";
import WorkflowCanvas from "@/components/workflows/WorkFlowCanvas";
import {
  INPUTNODE,
  OUTPUTNODE,
  type NODE_TYPES,
} from "@/configs/NodeTypeConfig";
import { NodeCreateOptionsList } from "@/configs/WorkflowNodesConfig";
import { NodeDataChangeContext } from "@/contexts/nodeDataChangeContext";
import { createNode } from "@/factories/NodeStateFactory";
import type { RootState } from "@/store/store";
import type { AllNodeType, FileMetaDataType } from "@/types/nodeDataTypes";
import { useEdgesState, useNodesState } from "@xyflow/react";
import { useCallback, useMemo } from "react";
import { useSelector } from "react-redux";
import { toast } from "react-toastify";

const CreateFlow = () => {
  const { nodes: savedNodes, edges: savedEdges } = useSelector(
    (state: RootState) => state.workflow
  );
  const [nodes, setNodesLocal, onNodesChange] =
    useNodesState<AllNodeType>(savedNodes);
  const [edges, setEdgesLocal, onEdgesChange] = useEdgesState(savedEdges);

  const addNodesToWF = useCallback(
    (nodeType: NODE_TYPES) => {
      setNodesLocal((prevNodes) => {
        if (
          nodeType === INPUTNODE &&
          prevNodes.some((n) => n.type === INPUTNODE)
        ) {
          toast.error("Only one Input Node is allowed");
          return prevNodes;
        }

        if (
          nodeType === OUTPUTNODE &&
          prevNodes.some((n) => n.type === OUTPUTNODE)
        ) {
          toast.error("Only one Output Node is allowed");
          return prevNodes;
        }
        const newNode = createNode(nodeType, (prevNodes.length + 1).toString());

        return [...prevNodes, newNode];
      });
    },
    [setNodesLocal]
  );

  function updateNodeData<T extends AllNodeType>(
    node: T,
    changedData: { id: string; value: string | number | FileMetaDataType[] }
  ): T {
    console.log("Updating node data:", node.id, changedData, node);

    return {
      ...node,
      data: {
        ...node.data,
        [changedData.id]: changedData.value,
      },
    };
  }
  const handleNodeDataChange = useCallback(
    (
      changedData: { id: string; value: string | number | FileMetaDataType[] },
      nodeId: string
    ) => {
      setNodesLocal((nds) => {
        return nds.map((n) =>
          n.id === nodeId ? updateNodeData(n, changedData) : n
        );
      });
    },
    [setNodesLocal]
  );
  const nodeDataChangeContextValue = useMemo(
    () => ({ handleNodeDataChange }),
    [handleNodeDataChange]
  );

  return (
    <>
      <SidebarLayout
        navbar={
          <CreateFlowSidebar
            nodeOptionsList={NodeCreateOptionsList}
            addNodesHandler={addNodesToWF}
          />
        }>
        <NodeDataChangeContext.Provider value={nodeDataChangeContextValue}>
          <WorkflowCanvas
            nodes={nodes}
            edges={edges}
            setNodes={setNodesLocal}
            setEdges={setEdgesLocal}
            onNodesChange={onNodesChange}
            onEdgesChange={onEdgesChange}
            handleNodeDataChange={handleNodeDataChange}
          />
        </NodeDataChangeContext.Provider>
      </SidebarLayout>
    </>
  );
};

export default CreateFlow;
