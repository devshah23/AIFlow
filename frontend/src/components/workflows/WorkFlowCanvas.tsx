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
import { useCallback, useState } from "react";
import { setWorkflow } from "@/store/slices/workflowSlice";

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
import workflowService from "@/apis/workflowService";
import { Spinner } from "../ui/spinner";
import workflowExecutionService from "@/apis/workflowExecutionService";
import isEqual from "lodash.isequal";

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
  const dispatch = useDispatch();
  const {
    edges: edgesStore,
    nodes: nodesStore,
    id: workflowId,
    name: workflowName,
    description: workflowDescription,
  } = useSelector((state: RootState) => state.workflow);
  const isValidConnection = useIsValidConnection(nodes, edges);
  const [executeLoading, setExecuteLoading] = useState(false);
  const [saveLoading, setSaveLoading] = useState(false);

  const saveWorkflowHandler = async () => {
    if (!workflowId && workflowId !== 0) {
      toast.error("Invalid Workflow ID. Cannot save.", { autoClose: 1000 });
      return;
    }

    setSaveLoading(true);

    try {
      const response = await workflowService.updateWorkflow(workflowId, {
        id: workflowId,
        name: workflowName,
        description: workflowDescription,
        nodes,
        edges,
      });

      if (response && response.success) {
        toast.success("Workflow saved successfully!", { autoClose: 500 });

        dispatch(setWorkflow(response.data));
      } else {
        const errorMsg = response?.message || "Failed to save workflow.";
        toast.error(errorMsg, { autoClose: 1000 });
      }
    } catch (error: any) {
      console.error("Error saving workflow:", error);

      const errorMessage =
        error?.response?.data?.message || "Connection error. Please try again.";
      toast.error(errorMessage, { autoClose: 2000 });
    } finally {
      setSaveLoading(false);
    }
  };
  const resetWorkflowHandler = () => {
    setNodesLocal(nodesStore);
    setEdgesLocal(edgesStore);
    toast.info("Workflow reset to last saved state.", { autoClose: 500 });
  };

  const executeWorkflowHandler = async () => {
    const areWorkflowEqual = () => {
      if (
        nodes.length !== nodesStore.length ||
        edges.length !== edgesStore.length
      ) {
        return false;
      }
      for (let i = 0; i < nodes.length; i++) {
        if (!isEqual(nodes[i].data, nodesStore[i].data)) {
          return false;
        }
      }
      return true;
    };

    if (!areWorkflowEqual() && !isEqual(edges, edgesStore)) {
      console.log(nodes, nodesStore, edges, edgesStore);
      toast.error("Please save the workflow before executing.", {
        autoClose: 1000,
      });
      return;
    }

    const inputNode = nodes.find((n) => n.type === INPUTNODE);
    if (!inputNode) {
      toast.error("Input Node is missing. Cannot execute workflow.", {
        autoClose: 1000,
      });
      return;
    }

    toast.info("Workflow execution started!", { autoClose: 500 });
    setExecuteLoading(true);

    try {
      const inputQuery = inputNode.data.query;

      const response = await workflowExecutionService.executeWorkflow(
        workflowId,
        inputQuery
      );

      if (response && response.success) {
        toast.success("Workflow executed successfully!", { autoClose: 500 });

        const output = response.data.output;

        // Update local nodes with the result
        const updatedNodes = nodesStore.map((node) =>
          node.type === OUTPUTNODE
            ? { ...node, data: { ...node.data, result: output } }
            : node
        );

        console.log("Workflow execution Updated Nodes:", updatedNodes);
        setNodesLocal(updatedNodes);
      } else {
        // Handle logic failure (API returned 200 but said success: false)
        throw new Error(response?.message || "Workflow execution failed.");
      }
    } catch (error: any) {
      console.error("Workflow Execution Error:", error);

      const errMsg =
        error?.response?.data?.message || error.message || "Execution failed";
      toast.error(errMsg, { autoClose: 2000 });
    } finally {
      console.log("Workflow execution Ended");
      setExecuteLoading(false);
    }
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
              onClick={saveWorkflowHandler}
              disabled={saveLoading}>
              {saveLoading ? <Spinner /> : ""}
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
            onClick={executeWorkflowHandler}
            disabled={executeLoading}
            variant="outline"
            size="icon-lg"
            className="rounded-full mr-10 mb-10 bg-green-500 hover:bg-green-400 *:text-white">
            {executeLoading ? <Spinner /> : <Play className="w-3 h-3" />}
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
