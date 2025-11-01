import {
  addEdge,
  Background,
  BackgroundVariant,
  ConnectionMode,
  Controls,
  Panel,
  ReactFlow,
  type Connection,
  type Edge,
  type Node,
  type OnDelete,
  type OnEdgesChange,
  type OnNodesChange,
} from "@xyflow/react";
import "@xyflow/react/dist/style.css";
import InputNode from "./nodes/InputNode";
import KnowledgeBaseNode from "./nodes/KnowledgeBaseNode";
import LLMNode from "./nodes/LLMNode";
import OutputNode from "./nodes/OutputNode";
import { useDispatch, useSelector } from "react-redux";
import { useCallback } from "react";
import { setEdges, setNodes } from "@/store/slices/workflowSlice";

import {
  INPUTNODE,
  KNOWLEDGEBASENODE,
  LLMNODE,
  OUTPUTNODE,
} from "@/configs/NodeTypeConfig";
import { Button } from "../ui/button";
import { toast } from "react-toastify";
import useIsValidConnection from "@/hooks/useIsValidConnection";
import type { RootState } from "@/store/store";
import type { AllNodeType } from "@/types/nodeDataTypes";
import { Play } from "lucide-react";

const nodeTypes = {
  [INPUTNODE]: InputNode,
  [KNOWLEDGEBASENODE]: KnowledgeBaseNode,
  [LLMNODE]: LLMNode,
  [OUTPUTNODE]: OutputNode,
};

type WorkFlowCanvasProps = {
  nodes: AllNodeType[];
  edges: Edge[];
  setNodes: React.Dispatch<React.SetStateAction<AllNodeType[]>>;
  setEdges: React.Dispatch<React.SetStateAction<Edge[]>>;
  onNodesChange: OnNodesChange<AllNodeType>;
  onEdgesChange: OnEdgesChange<Edge>;
  handleNodeDataChange?: (
    changedData: { id: string; value: string },
    nodeId: string
  ) => void;
};

const WorkFlowCanvas = ({
  nodes,
  edges,
  setNodes: setNodesLocal,
  setEdges: setEdgesLocal,
  onEdgesChange,
  onNodesChange,
}: WorkFlowCanvasProps) => {
  // My logic of saving the workflow is based on syncing local state with Redux only when user chooses to save.
  // This may lead to inconsistencies if user makes changes but doesn't save.
  const dispatch = useDispatch();
  const { edges: edgesStore, nodes: nodesStore } = useSelector(
    (state: RootState) => state.workflow
  );
  const isValidConnection = useIsValidConnection(nodes, edges);
  // TODO:Work of nodeStates with Save done here. Remaining reset, delete,updating localstate on node for each node type,removing context too.
  const saveWorkflowHandler = () => {
    dispatch(setNodes(nodes));
    dispatch(setEdges(edges));

    toast.success("Workflow saved successfully!", { autoClose: 500 });
  };

  const resetWorkflowHandler = () => {
    setNodesLocal(nodesStore);
    setEdgesLocal(edgesStore);
    toast.info("Workflow reset to last saved state.", { autoClose: 500 });
  };

  const onConnect = useCallback(
    (params: Connection) => {
      const newEdges = addEdge(params, edges);
      setEdgesLocal(newEdges);
    },
    [edges, setEdgesLocal]
  );
  const handleNodesChange: OnNodesChange<AllNodeType> = useCallback(
    (changes) => {
      onNodesChange(changes);
    },
    [onNodesChange]
  );

  const handleEdgesChange: OnEdgesChange<Edge> = useCallback(
    (changes) => {
      onEdgesChange(changes);
    },
    [onEdgesChange]
  );

  const onDelete: OnDelete<Node, Edge> = useCallback(
    (deletedElements) => {
      console.log("Deleted Elements:", deletedElements);
      if (deletedElements.nodes) {
        const newNodes = nodes.filter(
          (node) =>
            !deletedElements.nodes?.some(
              (deletedNode) => deletedNode.id === node.id
            )
        );
        setNodesLocal(newNodes);
      }
      if (deletedElements.edges) {
        const newEdges = edges.filter(
          (edge) =>
            !deletedElements.edges?.some(
              (deletedEdge) => deletedEdge.id === edge.id
            )
        );
        setEdgesLocal(newEdges);
      }
    },
    [edges, nodes, setNodesLocal, setEdgesLocal]
  );

  return (
    <div className="h-full w-full">
      <ReactFlow
        connectionMode={ConnectionMode.Strict}
        deleteKeyCode={["Delete", "Backspace"]}
        defaultViewport={{ x: 0, y: 0, zoom: 0.75 }}
        nodes={nodes}
        edges={edges}
        nodeTypes={nodeTypes}
        onNodesChange={handleNodesChange}
        onEdgesChange={handleEdgesChange}
        onConnect={onConnect}
        onDelete={onDelete}
        isValidConnection={isValidConnection}>
        <Panel position="top-right">
          <div className="flex gap-2">
            <Button
              variant="secondary"
              size="sm"
              className="bg-green-600 text-green-100 hover:bg-green-700 hover:text-white"
              onClick={saveWorkflowHandler}>
              Save
            </Button>
            <Button
              variant="secondary"
              size="sm"
              onClick={resetWorkflowHandler}
              className="text-accent bg-gray-500 hover:text-white hover:bg-gray-600">
              Reset
            </Button>
          </div>
        </Panel>
        <Panel position="bottom-right">
          <Button
            variant="outline"
            size="icon-lg"
            className="rounded-full mr-10 mb-10 bg-green-500 hover:bg-green-400 *:text-white">
            <Play className="w-3 h-3" />
          </Button>
        </Panel>
        <Controls />
        {/* <MiniMap /> */}
        <Background variant={BackgroundVariant.Cross} color="lightgray" />
      </ReactFlow>
    </div>
  );
};

export default WorkFlowCanvas;
