import {
  addEdge,
  Background,
  BackgroundVariant,
  ConnectionMode,
  Controls,
  ReactFlow,
  useEdgesState,
  useNodesState,
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
import type { RootState } from "@/store/store";

import {
  INPUTNODE,
  KNOWLEDGEBASENODE,
  LLMNODE,
  OUTPUTNODE,
} from "@/configs/NodeConfig";

const nodeTypes = {
  [INPUTNODE]: InputNode,
  [KNOWLEDGEBASENODE]: KnowledgeBaseNode,
  [LLMNODE]: LLMNode,
  [OUTPUTNODE]: OutputNode,
};

// const initialNodes = [
//   {
//     id: "1",
//     type: "input",
//     data: { label: "Input Node" },
//     position: { x: 250, y: 5 },
//   },
//   {
//     id: "2",
//     type: "knowledgeBase",
//     data: { label: "Knowledge Base Node" },
//     position: { x: 500, y: 100 },
//   },
//   {
//     id: "3",
//     type: "llmNode",
//     data: { label: "LLM Node" },
//     position: { x: 400, y: 300 },
//   },
//   {
//     id: "4",
//     type: "outputNode",
//     data: { label: "Output Node" },
//     position: { x: 600, y: 300 },
//   },
// ];

// const initialEdges = [
//   { id: "n1-n2", source: "1", target: "2" },
//   { id: "n1-n3", source: "2", target: "3" },
//   { id: "n1-n4", source: "1", target: "4" },
// ];

const FlowLayout = () => {
  // My logic of saving the workflow is based on syncing local state with Redux only when user chooses to save.
  // This may lead to inconsistencies if user makes changes but doesn't save.
  const dispatch = useDispatch();
  const { nodes: savedNodes, edges: savedEdges } = useSelector(
    (state: RootState) => state.workflow
  );

  // Local state synced with Redux
  const [nodes, setNodesLocal, onNodesChange] = useNodesState(savedNodes);
  const [edges, setEdgesLocal, onEdgesChange] = useEdgesState(savedEdges);
  const checkNodeCycle = useCallback(function checkCycle(
    source: string,
    target: string,
    edges: Edge[]
  ) {
    const visited = new Set();
    visited.add(source);
    visited.add(target);

    function dfs(node: string) {
      // if (node === source) return true;
      const nextNodes = edges
        .filter((e) => e.source === node)
        .map((e) => e.target);
      for (const n of nextNodes) {
        if (!visited.has(n)) {
          visited.add(n);
          return dfs(n);
        } else {
          return false;
        }
      }
      return true;
    }

    return dfs(target);
  },
  []);

  const isValidConnection = useCallback(
    (connection: Connection | Edge) => {
      console.log("Validating connection:", connection);
      console.log("Current nodes:", nodes);
      console.log("Current edges:", edges);
      if (connection.source == connection.target) return false;
      const targetNode = nodes.find((node) => node.id === connection.target);
      const sourceNode = nodes.find((node) => node.id === connection.source);
      if (!targetNode || !sourceNode) return false;
      if (sourceNode.type === OUTPUTNODE) return false;
      if (!checkNodeCycle(connection.source, connection.target, edges)) {
        console.log("Cycle detected");
        return false;
      }
      console.log("Connection valid");
      return true;
    },
    [nodes, edges, checkNodeCycle]
  );

  const onConnect = useCallback(
    (params: Connection) => {
      const newEdges = addEdge(params, edges);
      setEdgesLocal(newEdges);
    },
    [edges, setEdgesLocal]
  );
  const handleNodesChange: OnNodesChange<Node> = useCallback(
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
        dispatch(setNodes(newNodes));
      }
      if (deletedElements.edges) {
        const newEdges = edges.filter(
          (edge) =>
            !deletedElements.edges?.some(
              (deletedEdge) => deletedEdge.id === edge.id
            )
        );
        setEdgesLocal(newEdges);
        dispatch(setEdges(newEdges));
      }
    },
    [edges, nodes, setNodesLocal, setEdgesLocal, dispatch]
  );

  return (
    <div className="h-full w-full">
      <ReactFlow
        connectionMode={ConnectionMode.Strict}
        // defaultViewport={{ x: 0, y: 0, zoom: 0.8 }}
        nodes={nodes}
        edges={edges}
        nodeTypes={nodeTypes}
        onNodesChange={handleNodesChange}
        onEdgesChange={handleEdgesChange}
        // on={onConnectStart}
        onConnect={onConnect}
        onDelete={onDelete}
        isValidConnection={isValidConnection}
        // defaultEdgeOptions={{
        //   selectable: true,
        //   deletable: true,
        // }}
      >
        <Controls />
        {/* <MiniMap /> */}
        <Background variant={BackgroundVariant.Lines} />
      </ReactFlow>
    </div>
  );
};

export default FlowLayout;
