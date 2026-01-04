import {
  INPUTNODE,
  KNOWLEDGEBASENODE,
  LLMNODE,
  OUTPUTNODE,
} from "@/configs/NodeTypeConfig";
import { createNode } from "@/factories/NodeStateFactory";
import type {
  AllNodeType,
  InputNodeType,
  KnowledgeBaseNodeType,
  LLMNodeType,
  OutputNodeType,
} from "@/types/nodeDataTypes";
import type { WorkflowType } from "@/types/workflowTypes";
import { createSlice } from "@reduxjs/toolkit";
import type { PayloadAction } from "@reduxjs/toolkit";

const workflowMockData: WorkflowType = {
  // id: 99,
  // name: "New Workflow",
  // nodes: [
  //   createNode(INPUTNODE, "1", { x: 100, y: 150 }),
  //   createNode(KNOWLEDGEBASENODE, "2", { x: 350, y: 150 }),
  //   createNode(LLMNODE, "3", { x: 600, y: 150 }),
  //   createNode(OUTPUTNODE, "4", { x: 950, y: 150 }),
  // ],
  // edges: [
  //   // { id: "n1-n2", source: "1", target: "2" },
  //   // { id: "n1-n3", source: "2", target: "3" },
  //   // { id: "n1-n4", source: "1", target: "4" },
  // ],
} as WorkflowType;

export const workflow = createSlice({
  name: "workflow",
  initialState: workflowMockData,
  reducers: {
    setNodes: (state, action: PayloadAction<AllNodeType[]>) => {
      console.log("From store", action.payload);
      state.nodes = action.payload;
    },
    setEdges: (state, action: PayloadAction<WorkflowType["edges"]>) => {
      state.edges = action.payload;
    },
    setWorkflow: (state, action: PayloadAction<WorkflowType>) => {
      const desc = action.payload.description;
      const nodes = action.payload.nodes;
      state.id = action.payload.id;
      state.name = action.payload.name;
      state.description = desc && desc;
      state.nodes = nodes.map((n) => mapNodeToReduxType(n));
      state.edges = action.payload.edges;
    },
  },
});

function mapNodeToReduxType(n: AllNodeType) {
  console.log("Mapping node:", n);
  switch (n.type) {
    case INPUTNODE:
      console.log("Mapping INPUTNODE", n);
      return n as InputNodeType;
    case LLMNODE:
      console.log("Mapping LLMNODE", n);
      return n as LLMNodeType;
    case KNOWLEDGEBASENODE:
      console.log("Mapping KNOWLEDGEBASENODE", n);
      return n as KnowledgeBaseNodeType;
    case OUTPUTNODE:
      console.log("Mapping OUTPUTNODE", n);
      return n as OutputNodeType;
    default:
      throw new Error(`Unknown node type:`);
  }
}

export const { setNodes, setEdges, setWorkflow } = workflow.actions;
export default workflow.reducer;
