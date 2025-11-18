import {
  INPUTNODE,
  KNOWLEDGEBASENODE,
  LLMNODE,
  OUTPUTNODE,
} from "@/configs/NodeTypeConfig";
import { createNode } from "@/factories/NodeStateFactory";
import type { AllNodeType } from "@/types/nodeDataTypes";
import type { WorkflowType } from "@/types/workflowTypes";
import { createSlice } from "@reduxjs/toolkit";
import type { PayloadAction } from "@reduxjs/toolkit";

const workflowMockData: WorkflowType = {
  name: "New Workflow",
  nodes: [
    createNode(INPUTNODE, "1", { x: 100, y: 150 }),
    createNode(KNOWLEDGEBASENODE, "2", { x: 350, y: 150 }),
    createNode(LLMNODE, "3", { x: 600, y: 150 }),
    createNode(OUTPUTNODE, "4", { x: 950, y: 150 }),
  ],
  edges: [
    // { id: "n1-n2", source: "1", target: "2" },
    // { id: "n1-n3", source: "2", target: "3" },
    // { id: "n1-n4", source: "1", target: "4" },
  ],
};

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
      state.name = action.payload.name;
      state.nodes = action.payload.nodes;
      state.edges = action.payload.edges;
    },
  },
});

export const { setNodes, setEdges, setWorkflow } = workflow.actions;
export default workflow.reducer;
